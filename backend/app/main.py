from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
import json, os, uuid, csv, io
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session, joinedload
from pydantic import EmailStr
from .config import settings
from .database import Base, engine, get_db, SessionLocal
from .models import User, Bursary, Application, Document, AuditLog, Notification, ProfileDocument, EmailOTP
from .schemas import RegisterIn, VerifyOTPIn, LoginIn, TokenOut, UserOut, StaffUserIn, BursaryIn, BursaryOut, ApplicationIn, ApplicationOut, StatusIn, DocumentOut, ProfileUpdateIn, ProfileOut, ProfileDocumentOut
from .security import hash_password, verify_password, create_token, current_user, require_roles
from .email_service import (
    generate_otp,
    send_otp_email,
    send_application_submitted_email,
    send_application_status_changed_email,
    send_new_application_notification_to_reviewers
)

STATUSES = {"Submitted", "Under Review", "Verification", "Additional Information Required", "Committee Review", "Approved", "Rejected", "Disbursed"}
ALLOWED_EXT = {".pdf", ".jpg", ".jpeg", ".png"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    with SessionLocal() as db:
        if not db.scalar(select(Bursary.id).limit(1)):
            seeds = [
                Bursary(name="Constituency Development Bursary", description="Financial assistance for eligible secondary and tertiary learners.", eligibility="Needy student in secondary or tertiary school; constituency resident", amount_kes=15000, show_amount=True, deadline=date(2026,11,15), required_documents=json.dumps(["National ID or birth certificate","School or college admission letter","Fee structure","Parent or guardian income proof"])),
                Bursary(name="County Education Fund", description="County education support for eligible students.", eligibility="County resident enrolled in a recognised university or TVET college", amount_kes=25000, show_amount=True, deadline=date(2026,10,30), required_documents=json.dumps(["National ID","Student ID","Fee statement","Latest transcript"])),
                Bursary(name="Orphans and Vulnerable Learners Grant", description="Support for orphaned learners and learners from vulnerable households.", eligibility="Orphaned or from a vulnerable household; any recognised institution", amount_kes=40000, show_amount=True, deadline=date(2026,12,5), required_documents=json.dumps(["Birth certificate","Admission letter","Chief’s letter","Fee structure"])),
                Bursary(name="STEM Merit Bursary", description="Support for learners pursuing science, engineering and ICT courses.", eligibility="Year 2 or above in a science, engineering or ICT course; mean grade B or higher", amount_kes=30000, show_amount=True, deadline=date(2026,9,20), required_documents=json.dumps(["National ID","Student ID","Transcript"]))]
            db.add_all(seeds); db.commit()
        admin_email = os.getenv("ADMIN_EMAIL", "admin@smartbursary.com").lower()
        admin_password = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")
        if not db.scalar(select(User.id).where(User.email == admin_email)):
            db.add(User(full_name="SmartBursary Administrator", email=admin_email, password_hash=hash_password(admin_password), role="admin", phone="")); db.commit()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", description="SmartBursary applications, review and tracking API", lifespan=lifespan)

# CORS Middleware - allows frontend from different domains
allowed_origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=allowed_origins,
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

def audit(db: Session, actor: User | None, action: str, entity_type="", entity_id="", details=""):
    db.add(AuditLog(actor_id=actor.id if actor else None, actor_name=actor.full_name if actor else "System", action=action, entity_type=entity_type, entity_id=str(entity_id), details=details))

def bursary_out(b: Bursary):
    return {"id":b.id,"name":b.name,"description":b.description,"eligibility":b.eligibility,"constituency":b.constituency,"amount_kes":b.amount_kes,"show_amount":b.show_amount,"deadline":b.deadline,"required_documents":json.loads(b.required_documents or "[]"),"active":b.active}

def application_out(a: Application):
    return {"id":a.id,"application_number":a.application_number,"applicant_id":a.applicant_id,"applicant_name":a.applicant.full_name,"applicant_email":a.applicant.email,"bursary_id":a.bursary_id,"bursary_name":a.bursary.name,"amount_kes":a.bursary.amount_kes,"show_amount":a.bursary.show_amount,"institution":a.institution,"student_number":a.student_number,"national_id":a.national_id,"monthly_household_income":a.monthly_household_income,"household_size":a.household_size,"course":a.course,"year_of_study":a.year_of_study,"reason":a.reason,"status":a.status,"priority_score":a.priority_score,"financial_need":a.financial_need,"education_need":a.education_need,"duplicate_risk":a.duplicate_risk,"reviewer_comment":a.reviewer_comment,"submitted_at":a.submitted_at,"updated_at":a.updated_at,"documents":a.documents}

def app_query(db):
    return select(Application).options(joinedload(Application.applicant), joinedload(Application.bursary), joinedload(Application.documents))

def priority(income: int, household: int, duplicate: bool):
    # Transparent demo heuristic only; it is not an eligibility or award decision.
    score = 50 + round((1 - min(income / 60000, 1)) * 35) + (8 if household > 4 else 0)
    if duplicate: score = min(score, 45)
    return min(95, max(0, score)), ("HIGH" if income < 20000 else "MEDIUM"), ("HIGH" if duplicate else "LOW")

@app.get("/api/health")
def health(): return {"status":"ok","service":"SmartBursary API"}

@app.post("/api/auth/register", status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    """Register a new user and send OTP for email verification."""
    email = str(data.email).lower()
    
    # Check if user already exists
    if db.scalar(select(User.id).where(User.email == email)):
        raise HTTPException(409, "An account with this email already exists")
    
    # Create user but mark as unverified
    user = User(
        full_name=data.full_name.strip(),
        email=email,
        phone=data.phone.strip(),
        password_hash=hash_password(data.password),
        role="applicant",
        email_verified=False,
        active=False  # Account inactive until email verified
    )
    db.add(user)
    db.flush()
    
    # Generate and store OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Remove any existing OTPs for this email
    db.execute(select(EmailOTP).where(EmailOTP.email == email)).scalars().all()
    for old_otp in db.scalars(select(EmailOTP).where(EmailOTP.email == email)).all():
        db.delete(old_otp)
    
    otp = EmailOTP(
        email=email,
        otp_code=otp_code,
        purpose="registration",
        expires_at=expires_at
    )
    db.add(otp)
    
    audit(db, None, "User registered (pending verification)", "User", user.id, email)
    db.commit()
    
    # Send OTP email
    send_otp_email(email, user.full_name, otp_code)
    
    return {
        "message": "Registration successful. Please check your email for the verification code.",
        "email": email,
        "requires_verification": True
    }

@app.post("/api/auth/verify-otp", response_model=TokenOut)
def verify_otp(data: VerifyOTPIn, db: Session = Depends(get_db)):
    """Verify OTP and activate user account."""
    email = str(data.email).lower()
    
    # Find user
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(404, "User not found")
    
    if user.email_verified:
        raise HTTPException(400, "Email already verified")
    
    # Find valid OTP
    otp = db.scalar(
        select(EmailOTP)
        .where(
            EmailOTP.email == email,
            EmailOTP.otp_code == data.otp_code,
            EmailOTP.purpose == "registration",
            EmailOTP.verified == False,
            EmailOTP.expires_at > datetime.utcnow()
        )
        .order_by(EmailOTP.created_at.desc())
    )
    
    if not otp:
        raise HTTPException(400, "Invalid or expired verification code")
    
    # Mark OTP as verified
    otp.verified = True
    
    # Activate user account
    user.email_verified = True
    user.active = True
    
    audit(db, user, "Email verified and account activated", "User", user.id)
    db.commit()
    db.refresh(user)
    
    return {"access_token": create_token(user), "user": user}

@app.post("/api/auth/resend-otp", status_code=200)
def resend_otp(email: EmailStr, db: Session = Depends(get_db)):
    """Resend OTP code to user's email."""
    email_lower = str(email).lower()
    
    user = db.scalar(select(User).where(User.email == email_lower))
    if not user:
        raise HTTPException(404, "User not found")
    
    if user.email_verified:
        raise HTTPException(400, "Email already verified")
    
    # Generate new OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Invalidate old OTPs
    for old_otp in db.scalars(select(EmailOTP).where(EmailOTP.email == email_lower)).all():
        db.delete(old_otp)
    
    otp = EmailOTP(
        email=email_lower,
        otp_code=otp_code,
        purpose="registration",
        expires_at=expires_at
    )
    db.add(otp)
    db.commit()
    
    # Send new OTP
    send_otp_email(email_lower, user.full_name, otp_code)
    
    return {"message": "Verification code resent successfully"}

@app.post("/api/auth/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(data.email).lower()))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Email or password is incorrect")
    if not user.active: raise HTTPException(403,"This account is disabled")
    return {"access_token":create_token(user),"user":user}

@app.get("/api/auth/me", response_model=UserOut)
def me(user: User = Depends(current_user)): return user

@app.get("/api/profile", response_model=ProfileOut)
def get_profile(db: Session = Depends(get_db), user: User = Depends(current_user)):
    user_with_docs = db.scalars(select(User).options(joinedload(User.profile_documents)).where(User.id == user.id)).unique().first()
    return user_with_docs

@app.patch("/api/profile", response_model=ProfileOut)
async def update_profile(request: Request, db: Session = Depends(get_db), user: User = Depends(current_user)):
    # Get raw JSON data without validation
    try:
        data = await request.json()
    except:
        data = {}
    
    # Handle date parsing from various formats
    if 'date_of_birth' in data and data['date_of_birth']:
        dob = data['date_of_birth']
        if isinstance(dob, str):
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                try:
                    data['date_of_birth'] = datetime.strptime(dob, fmt).date()
                    break
                except ValueError:
                    continue
    
    # Map of string fields
    string_fields = ["national_id", "gender", "county", "sub_county", "address", "guardian_name", "guardian_phone", "guardian_relationship", "institution", "student_number", "course", "year_of_study"]
    
    for key, value in data.items():
        if key in string_fields:
            setattr(user, key, value or "")
        elif key == 'date_of_birth':
            setattr(user, key, value)
        elif key == 'admission_year':
            if isinstance(value, int) and value > 0:
                setattr(user, key, value)
        elif key in ['monthly_household_income', 'household_size']:
            if value is not None:
                try:
                    setattr(user, key, int(value))
                except (ValueError, TypeError):
                    pass
    
    # Check if profile is complete
    required_fields = [
        user.date_of_birth is not None,
        bool(user.national_id.strip()),
        bool(user.gender.strip()),
        bool(user.county.strip()),
        bool(user.constituency.strip()),
        bool(user.institution.strip()),
        bool(user.student_number.strip()),
        bool(user.course.strip()),
        bool(user.year_of_study.strip()),
        user.monthly_household_income > 0,
        user.household_size > 0,
        user.has_national_id_doc,
        user.has_student_id_doc
    ]
    user.profile_complete = all(required_fields)
    
    audit(db, user, "Updated profile", "User", user.id)
    db.commit()
    user_with_docs = db.scalars(select(User).options(joinedload(User.profile_documents)).where(User.id == user.id)).unique().first()
    return user_with_docs

@app.post("/api/profile/documents", response_model=ProfileDocumentOut, status_code=201)
async def upload_profile_document(document_type: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    if document_type not in ["National ID", "Student ID", "Admission Letter", "Birth Certificate", "Transcript"]:
        raise HTTPException(400, "Invalid document type")
    
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(400, "Only PDF, JPG and PNG files are accepted")
    
    content = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if not content:
        raise HTTPException(400, "The selected file is empty")
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb} MB")
    
    # Delete existing document of same type
    existing = db.scalars(select(ProfileDocument).where(
        ProfileDocument.user_id == user.id,
        ProfileDocument.document_type == document_type
    )).first()
    if existing:
        old_path = Path(settings.upload_dir) / existing.stored_filename
        if old_path.exists():
            old_path.unlink()
        db.delete(existing)
    
    stored = f"profile_{uuid.uuid4().hex}{suffix}"
    folder = Path(settings.upload_dir)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / stored).write_bytes(content)
    
    doc = ProfileDocument(
        user_id=user.id,
        document_type=document_type,
        original_filename=Path(file.filename or "upload").name[:255],
        stored_filename=stored,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(content)
    )
    db.add(doc)
    
    # Update document flags
    if document_type == "National ID":
        user.has_national_id_doc = True
    elif document_type == "Student ID":
        user.has_student_id_doc = True
    elif document_type == "Admission Letter":
        user.has_admission_letter = True
    
    audit(db, user, f"Uploaded profile document: {document_type}", "ProfileDocument", doc.id)
    db.commit()
    db.refresh(doc)
    return doc

@app.get("/api/profile/documents/{document_id}/download")
def download_profile_document(document_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc = db.get(ProfileDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    if doc.user_id != user.id and user.role not in ["admin", "reviewer"]:
        raise HTTPException(403, "You cannot access this document")
    
    path = Path(settings.upload_dir) / doc.stored_filename
    if not path.exists():
        raise HTTPException(404, "File is missing from storage")
    return FileResponse(path, filename=doc.original_filename, media_type=doc.content_type)

@app.delete("/api/profile/documents/{document_id}")
def delete_profile_document(document_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc = db.get(ProfileDocument, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    if doc.user_id != user.id:
        raise HTTPException(403, "You can only delete your own documents")
    
    # Update document flags
    if doc.document_type == "National ID":
        user.has_national_id_doc = False
    elif doc.document_type == "Student ID":
        user.has_student_id_doc = False
    elif doc.document_type == "Admission Letter":
        user.has_admission_letter = False
    
    # Delete file from storage
    path = Path(settings.upload_dir) / doc.stored_filename
    if path.exists():
        path.unlink()
    
    audit(db, user, f"Deleted profile document: {doc.document_type}", "ProfileDocument", doc.id)
    db.delete(doc)
    db.commit()
    return {"ok": True}

@app.post("/api/admin/users", response_model=UserOut, status_code=201)
def create_staff_user(data: StaffUserIn, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    email = str(data.email).lower()
    if db.scalar(select(User.id).where(User.email == email)):
        raise HTTPException(409, "An account with this email already exists")
    staff_user = User(full_name=data.full_name.strip(), email=email, password_hash=hash_password(data.password), role=data.role, active=True)
    db.add(staff_user); db.flush(); audit(db, user, f"Created {data.role} account", "User", staff_user.id, email); db.commit(); db.refresh(staff_user)
    return staff_user

@app.get("/api/bursaries", response_model=list[BursaryOut])
def list_bursaries(include_inactive: bool = False, constituency: str = "", search: str = "", db: Session = Depends(get_db), user: User = Depends(current_user)):
    q = select(Bursary).order_by(Bursary.deadline)
    if not include_inactive or user.role == "applicant": q = q.where(Bursary.active.is_(True))
    
    # Applicants can VIEW all bursaries (no filtering) for transparency
    # But they can only APPLY to their constituency (enforced in create_application)
    
    # Auto-filter for constituency admins and reviewers
    if user.constituency and user.role in ("admin", "reviewer"):
        q = q.where(Bursary.constituency == user.constituency)
    # Allow manual constituency filter for super admin
    elif constituency.strip():
        q = q.where(Bursary.constituency.ilike(f"%{constituency.strip()}%"))
    
    if search.strip():
        search_term = f"%{search.strip()}%"
        q = q.where(or_(Bursary.name.ilike(search_term), Bursary.description.ilike(search_term), Bursary.eligibility.ilike(search_term), Bursary.constituency.ilike(search_term)))
    return [bursary_out(x) for x in db.scalars(q).all()]

@app.get("/api/bursaries/constituencies")
def get_constituencies(db: Session = Depends(get_db)):
    """Get list of all unique constituencies with bursary count"""
    results = db.execute(select(Bursary.constituency, func.count(Bursary.id).label('count')).where(Bursary.active.is_(True)).group_by(Bursary.constituency)).fetchall()
    return [{"constituency": r[0] or "General", "count": r[1]} for r in results if r[0]]

@app.post("/api/bursaries", response_model=BursaryOut, status_code=201)
def create_bursary(data: BursaryIn, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    # Constituency admins can only create bursaries for their constituency
    if user.constituency and data.constituency != user.constituency:
        raise HTTPException(403, "You can only create bursaries for your constituency")
    if db.scalar(select(Bursary.id).where(Bursary.name == data.name)): raise HTTPException(409,"A bursary with this name already exists")
    b=Bursary(name=data.name,description=data.description,eligibility=data.eligibility,amount_kes=data.amount_kes,show_amount=data.show_amount,deadline=data.deadline,required_documents=json.dumps(data.required_documents),active=data.active,constituency=data.constituency)
    db.add(b);db.flush();audit(db,user,"Created bursary","Bursary",b.id,b.name);db.commit();db.refresh(b);return bursary_out(b)

@app.patch("/api/bursaries/{bursary_id}", response_model=BursaryOut)
def update_bursary(bursary_id:int,data:BursaryIn,db:Session=Depends(get_db),user:User=Depends(require_roles("admin"))):
    b=db.get(Bursary,bursary_id)
    if not b: raise HTTPException(404,"Bursary not found")
    # Constituency admins can only update bursaries from their constituency
    if user.constituency and b.constituency != user.constituency:
        raise HTTPException(403, "You can only update bursaries from your constituency")
    for k,v in data.model_dump().items(): setattr(b,k,json.dumps(v) if k=="required_documents" else v)
    audit(db,user,"Updated bursary","Bursary",b.id,b.name);db.commit();db.refresh(b);return bursary_out(b)

@app.patch("/api/bursaries/{bursary_id}/toggle")
def toggle_bursary(bursary_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    b = db.get(Bursary, bursary_id)
    if not b: raise HTTPException(404, "Bursary not found")
    # Constituency admins can only toggle bursaries from their constituency
    if user.constituency and b.constituency != user.constituency:
        raise HTTPException(403, "You can only toggle bursaries from your constituency")
    b.active = not b.active
    action = "Opened" if b.active else "Closed"
    audit(db, user, f"{action} bursary applications", "Bursary", b.id, b.name)
    db.commit()
    db.refresh(b)
    return bursary_out(b)

@app.get("/api/staff", response_model=list[UserOut])
def list_staff(db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    """List staff users - filtered by constituency for constituency admins"""
    query = select(User).where(User.role.in_(["admin", "reviewer"]))
    
    # If admin has a constituency, only show staff from that constituency
    if user.constituency:
        query = query.where(User.constituency == user.constituency)
    
    staff = db.scalars(query.order_by(User.full_name)).all()
    return staff

@app.post("/api/staff", response_model=UserOut, status_code=201)
def create_staff_user(data: StaffUserIn, db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    """Create a new staff user - constituency admins can only create staff for their constituency"""
    email = str(data.email).lower()
    if db.scalar(select(User.id).where(User.email == email)):
        raise HTTPException(409, "An account with this email already exists")
    
    # If admin has a constituency, enforce they can only create staff for their constituency
    if user.constituency and data.constituency != user.constituency:
        raise HTTPException(403, f"You can only create staff for your constituency ({user.constituency})")
    
    # Constituency admins can only create reviewers, not other admins
    if user.constituency and data.role == "admin":
        raise HTTPException(403, "Constituency admins cannot create other admin accounts")
    
    staff_user = User(
        full_name=data.full_name.strip(),
        email=email,
        password_hash=hash_password(data.password),
        role=data.role,
        constituency=data.constituency,
        active=True,
        email_verified=True  # Staff accounts are pre-verified
    )
    db.add(staff_user)
    db.flush()
    audit(db, user, f"Created {data.role} account", "User", staff_user.id, email)
    db.commit()
    db.refresh(staff_user)
    return staff_user


@app.post("/api/applications", response_model=ApplicationOut, status_code=201)
def submit_application(data:ApplicationIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    # Check if profile is complete
    if not user.profile_complete:
        raise HTTPException(403, "Please complete your profile before applying for bursaries")
    
    b=db.get(Bursary,data.bursary_id)
    if not b or not b.active: raise HTTPException(404,"Active bursary not found")
    if b.deadline < date.today(): raise HTTPException(400,"The deadline for this bursary has passed")
    
    # Constituency eligibility check: applicants can only apply to their home constituency
    if user.role == "applicant" and user.constituency and b.constituency:
        if user.constituency != b.constituency:
            raise HTTPException(403, f"You can only apply to bursaries in your home constituency ({user.constituency}). This bursary is for {b.constituency}.")
    
    # Use profile data if not provided in application
    institution = data.institution.strip() or user.institution
    student_number = data.student_number.strip() or user.student_number
    national_id = data.national_id.strip() or user.national_id
    course = data.course.strip() or user.course
    year_of_study = data.year_of_study.strip() or user.year_of_study
    monthly_household_income = data.monthly_household_income if data.monthly_household_income > 0 else user.monthly_household_income
    household_size = data.household_size if data.household_size > 1 else user.household_size
    
    duplicate = db.scalar(select(Application.id).where(or_(Application.student_number==student_number, (Application.national_id==national_id) if national_id else False)).limit(1)) is not None
    score,fin,dup=priority(monthly_household_income,household_size,duplicate)
    count=db.scalar(select(func.count(Application.id))) or 0
    number=f"SB-{datetime.now().year}-{count+1:05d}"
    while db.scalar(select(Application.id).where(Application.application_number==number)): number=f"SB-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
    a=Application(application_number=number,applicant_id=user.id,bursary_id=b.id,institution=institution,student_number=student_number,national_id=national_id,monthly_household_income=monthly_household_income,household_size=household_size,course=course,year_of_study=year_of_study,reason=data.reason.strip(),priority_score=score,financial_need=fin,duplicate_risk=dup)
    db.add(a);db.flush();db.add(Notification(user_id=user.id,title="Application submitted",message=f"Your application {number} has been submitted."));audit(db,user,"Submitted application","Application",a.id,number);db.commit()
    
    # Send email notifications
    send_application_submitted_email(user.email, user.full_name, b.name, number)
    
    # Notify reviewers in the same constituency
    if b.constituency:
        reviewers = db.scalars(select(User).where(
            User.role == "reviewer",
            User.constituency == b.constituency,
            User.active == True
        )).all()
        reviewer_emails = [r.email for r in reviewers if r.email]
        if reviewer_emails:
            send_new_application_notification_to_reviewers(
                reviewer_emails, b.name, user.full_name, b.constituency, number
            )
    
    a=db.scalars(app_query(db).where(Application.id==a.id)).unique().first();return application_out(a)

@app.get("/api/applications", response_model=list[ApplicationOut])
def list_applications(q:str="",status_filter:str="",db:Session=Depends(get_db),user:User=Depends(current_user)):
    query=app_query(db)
    if user.role == "applicant": query=query.where(Application.applicant_id==user.id)
    # Filter by constituency for reviewers and constituency admins
    elif user.constituency and user.role in ("reviewer", "admin"):
        query = query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    if status_filter: query=query.where(Application.status==status_filter)
    if q.strip():
        like=f"%{q.strip()}%"; query=query.join(Application.applicant).where(or_(Application.application_number.ilike(like),Application.institution.ilike(like),Application.student_number.ilike(like),User.full_name.ilike(like)))
    return [application_out(a) for a in db.scalars(query.order_by(Application.submitted_at.desc())).unique().all()]

@app.get("/api/applications/{application_number}", response_model=ApplicationOut)
def get_application(application_number:str,db:Session=Depends(get_db),user:User=Depends(current_user)):
    a=db.scalars(app_query(db).where(Application.application_number==application_number)).unique().first()
    if not a: raise HTTPException(404,"Application not found")
    if user.role=="applicant" and a.applicant_id!=user.id: raise HTTPException(403,"You can only view your own applications")
    # Constituency admins and reviewers can only view applications from their constituency
    if user.constituency and user.role in ("admin", "reviewer") and a.bursary.constituency != user.constituency:
        raise HTTPException(403, "You can only view applications from your constituency")
    return application_out(a)

@app.patch("/api/applications/{application_number}/status", response_model=ApplicationOut)
def update_status(application_number:str,data:StatusIn,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","reviewer"))):
    if data.status not in STATUSES: raise HTTPException(400,"Unsupported application status")
    a=db.scalars(app_query(db).where(Application.application_number==application_number)).unique().first()
    if not a: raise HTTPException(404,"Application not found")
    # Constituency admins and reviewers can only update applications from their constituency
    if user.constituency and user.role in ("admin", "reviewer") and a.bursary.constituency != user.constituency:
        raise HTTPException(403, "You can only update applications from your constituency")
    old=a.status;a.status=data.status;a.reviewer_comment=data.reviewer_comment
    db.add(Notification(user_id=a.applicant_id,title="Application status updated",message=f"{a.application_number}: {old} → {a.status}"));audit(db,user,f"Changed status from {old} to {a.status}","Application",a.id,data.reviewer_comment);db.commit()
    
    # Send email notification to applicant
    send_application_status_changed_email(
        a.applicant.email,
        a.applicant.full_name,
        a.bursary.name,
        a.application_number,
        a.status,
        a.bursary.amount_kes if a.status.lower() in ["approved", "disbursed"] else None
    )
    
    a=db.scalars(app_query(db).where(Application.id==a.id)).unique().first();return application_out(a)

@app.post("/api/applications/{application_number}/documents", response_model=DocumentOut, status_code=201)
async def upload_document(application_number:str,document_type:str=Form(...),file:UploadFile=File(...),db:Session=Depends(get_db),user:User=Depends(current_user)):
    a=db.scalar(select(Application).where(Application.application_number==application_number))
    if not a: raise HTTPException(404,"Application not found")
    if user.role=="applicant" and a.applicant_id!=user.id: raise HTTPException(403,"You can only upload to your own application")
    suffix=Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT: raise HTTPException(400,"Only PDF, JPG and PNG files are accepted")
    content=await file.read(settings.max_upload_mb*1024*1024+1)
    if not content: raise HTTPException(400,"The selected file is empty")
    if len(content)>settings.max_upload_mb*1024*1024: raise HTTPException(413,f"File exceeds {settings.max_upload_mb} MB")
    stored=f"{uuid.uuid4().hex}{suffix}";folder=Path(settings.upload_dir);folder.mkdir(parents=True,exist_ok=True);(folder/stored).write_bytes(content)
    doc=Document(application_id=a.id,document_type=document_type[:180],original_filename=Path(file.filename or "upload").name[:255],stored_filename=stored,content_type=file.content_type or "application/octet-stream",size_bytes=len(content))
    db.add(doc);audit(db,user,"Uploaded document","Application",a.id,document_type);db.commit();db.refresh(doc);return doc

@app.get("/api/documents/{document_id}/download")
def download_document(document_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    doc=db.get(Document,document_id)
    if not doc: raise HTTPException(404,"Document not found")
    a=db.get(Application,doc.application_id)
    if user.role=="applicant" and a.applicant_id!=user.id: raise HTTPException(403,"You cannot access this document")
    path=Path(settings.upload_dir)/doc.stored_filename
    if not path.exists(): raise HTTPException(404,"File is missing from storage")
    return FileResponse(path,filename=doc.original_filename,media_type=doc.content_type)

@app.patch("/api/documents/{document_id}/verification", response_model=DocumentOut)
def verify_document(document_id:int,status_value:str=Query(...,alias="status"),db:Session=Depends(get_db),user:User=Depends(require_roles("admin","reviewer"))):
    if status_value not in {"Pending","Verified","Rejected","More information required"}: raise HTTPException(400,"Unsupported verification status")
    d=db.get(Document,document_id)
    if not d: raise HTTPException(404,"Document not found")
    d.verification_status=status_value;audit(db,user,f"Set document verification to {status_value}","Document",d.id);db.commit();db.refresh(d);return d

@app.get("/api/dashboard/stats")
def dashboard_stats(db:Session=Depends(get_db),user:User=Depends(require_roles("admin","reviewer"))):
    # Base query for stats
    base_query = select(func.count(Application.id))
    # Filter by constituency for reviewers
    if user.role == "reviewer" and user.constituency:
        base_query = base_query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    total=db.scalar(base_query) or 0
    statuses={}
    for s in sorted(STATUSES):
        status_query = select(func.count(Application.id)).where(Application.status==s)
        if user.role == "reviewer" and user.constituency:
            status_query = status_query.join(Application.bursary).where(Bursary.constituency == user.constituency)
        statuses[s] = db.scalar(status_query) or 0
    
    duplicate_query = select(func.count(Application.id)).where(Application.duplicate_risk=="HIGH")
    if user.role == "reviewer" and user.constituency:
        duplicate_query = duplicate_query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    return {"total":total,"pending":sum(statuses[s] for s in ["Submitted","Under Review","Verification","Additional Information Required","Committee Review"]),"duplicate_flags":db.scalar(duplicate_query) or 0,"statuses":statuses,"bursaries":db.scalar(select(func.count(Bursary.id)).where(Bursary.active.is_(True))) or 0}

@app.get("/api/reports/applications.csv")
def report_csv(db:Session=Depends(get_db),user:User=Depends(require_roles("admin","reviewer"))):
    apps=db.scalars(app_query(db).order_by(Application.submitted_at.desc())).unique().all();s=io.StringIO();w=csv.writer(s)
    w.writerow(["Application number","Applicant","Email","Bursary","Institution","Student number","Status","Priority score","Financial need","Duplicate risk","Submitted at"])
    for a in apps:w.writerow([a.application_number,a.applicant.full_name,a.applicant.email,a.bursary.name,a.institution,a.student_number,a.status,a.priority_score,a.financial_need,a.duplicate_risk,a.submitted_at.isoformat()])
    return StreamingResponse(iter([s.getvalue()]),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=smartbursary-applications.csv"})

@app.get("/api/audit")
def audit_logs(limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db),user:User=Depends(require_roles("admin"))):
    rows=db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)).all()
    return [{"id":x.id,"actor_name":x.actor_name,"action":x.action,"entity_type":x.entity_type,"entity_id":x.entity_id,"details":x.details,"created_at":x.created_at} for x in rows]

@app.get("/api/notifications")
def notifications(db:Session=Depends(get_db),user:User=Depends(current_user)):
    rows=db.scalars(select(Notification).where(Notification.user_id==user.id).order_by(Notification.created_at.desc()).limit(50)).all()
    return [{"id":x.id,"title":x.title,"message":x.message,"read":x.read,"created_at":x.created_at} for x in rows]

@app.patch("/api/notifications/{notification_id}/read")
def mark_notification_read(notification_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    n=db.get(Notification,notification_id)
    if not n or n.user_id!=user.id: raise HTTPException(404,"Notification not found")
    n.read=True;db.commit();return {"ok":True}



@app.get("/api/reports/overview")
def get_reports_overview(db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "reviewer"))):
    """Get comprehensive reports and analytics data."""
    # Base applications query
    apps_query = select(Application).options(joinedload(Application.bursary))
    if user.role == "reviewer" and user.constituency:
        apps_query = apps_query.join(Application.bursary).where(Bursary.constituency == user.constituency)
    
    all_apps = list(db.scalars(apps_query).unique().all())
    
    # Overall stats
    total_apps = len(all_apps)
    approved = len([a for a in all_apps if a.status == "Approved"])
    rejected = len([a for a in all_apps if a.status == "Rejected"])
    pending = len([a for a in all_apps if a.status in ["Submitted", "Under Review", "Verification", "Committee Review"]])
    disbursed = len([a for a in all_apps if a.status == "Disbursed"])
    
    # Total disbursed amount
    total_disbursed = sum([a.bursary.amount_kes for a in all_apps if a.status == "Disbursed"])
    
    # Applications by constituency
    constituency_data = {}
    for app in all_apps:
        const = app.bursary.constituency or "Unspecified"
        if const not in constituency_data:
            constituency_data[const] = {"total": 0, "approved": 0, "pending": 0, "disbursed": 0, "amount": 0}
        constituency_data[const]["total"] += 1
        if app.status == "Approved":
            constituency_data[const]["approved"] += 1
        if app.status in ["Submitted", "Under Review", "Verification", "Committee Review"]:
            constituency_data[const]["pending"] += 1
        if app.status == "Disbursed":
            constituency_data[const]["disbursed"] += 1
            constituency_data[const]["amount"] += app.bursary.amount_kes
    
    # Applications by status
    status_data = {}
    for status in STATUSES:
        count = len([a for a in all_apps if a.status == status])
        status_data[status] = count
    
    # Applications by bursary
    bursary_data = {}
    for app in all_apps:
        bursary_name = app.bursary.name
        if bursary_name not in bursary_data:
            bursary_data[bursary_name] = {"total": 0, "approved": 0, "avg_amount": app.bursary.amount_kes}
        bursary_data[bursary_name]["total"] += 1
        if app.status == "Approved" or app.status == "Disbursed":
            bursary_data[bursary_name]["approved"] += 1
    
    return {
        "summary": {
            "total_applications": total_apps,
            "approved": approved,
            "rejected": rejected,
            "pending": pending,
            "disbursed": disbursed,
            "total_disbursed_amount": total_disbursed,
            "approval_rate": round((approved / total_apps * 100) if total_apps > 0 else 0, 1)
        },
        "by_constituency": [
            {"constituency": k, **v, "approval_rate": round((v["approved"] / v["total"] * 100) if v["total"] > 0 else 0, 1)}
            for k, v in sorted(constituency_data.items())
        ],
        "by_status": [{"status": k, "count": v, "percentage": round((v / total_apps * 100) if total_apps > 0 else 0, 1)} for k, v in status_data.items()],
        "by_bursary": [
            {"bursary": k, **v, "approval_rate": round((v["approved"] / v["total"] * 100) if v["total"] > 0 else 0, 1)}
            for k, v in sorted(bursary_data.items(), key=lambda x: x[1]["total"], reverse=True)
        ]
    }
