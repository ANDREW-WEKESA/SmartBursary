"""Setup 3 accounts for local presentation"""
from app.database import SessionLocal
from app.models import User
from app.security import hash_password

db = SessionLocal()

try:
    print("Setting up accounts for LOCAL presentation...")
    print("")
    
    # 1. Check/Create Admin
    admin = db.query(User).filter_by(email='admin@smartbursary.com').first()
    if admin:
        print("✅ Admin already exists")
    else:
        admin = User(
            full_name="System Administrator",
            email="admin@smartbursary.com",
            password_hash=hash_password("admin123"),
            role="admin",
            phone="0700000000",
            email_verified=True,
            active=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin created")
    
    # 2. Check/Create Reviewer
    reviewer = db.query(User).filter_by(email='reviewer@smartbursary.com').first()
    if reviewer:
        # Make sure it's actually a reviewer
        if reviewer.role != "reviewer":
            reviewer.role = "reviewer"
            db.commit()
            print("✅ Reviewer account fixed (was applicant, now reviewer)")
        else:
            print("✅ Reviewer already exists")
    else:
        reviewer = User(
            full_name="Jane Reviewer",
            email="reviewer@smartbursary.com",
            password_hash=hash_password("reviewer123"),
            role="reviewer",
            phone="0722334455",
            email_verified=True,
            active=True
        )
        db.add(reviewer)
        db.commit()
        print("✅ Reviewer created")
    
    # 3. Check/Create Applicant
    applicant = db.query(User).filter_by(email='student@smartbursary.com').first()
    if applicant:
        print("✅ Applicant already exists")
    else:
        applicant = User(
            full_name="John Student",
            email="student@smartbursary.com",
            password_hash=hash_password("student123"),
            role="applicant",
            phone="0733445566",
            email_verified=True,
            active=True
        )
        db.add(applicant)
        db.commit()
        print("✅ Applicant created")
    
    print("")
    print("="*60)
    print("✅ LOCAL ACCOUNTS READY FOR PRESENTATION!")
    print("="*60)
    print("")
    print("URL: http://localhost:5174/")
    print("")
    print("1. ADMIN:")
    print("   Email: admin@smartbursary.com")
    print("   Password: admin123")
    print("")
    print("2. REVIEWER:")
    print("   Email: reviewer@smartbursary.com")
    print("   Password: reviewer123")
    print("")
    print("3. APPLICANT:")
    print("   Email: student@smartbursary.com")
    print("   Password: student123")
    print("")
    print("="*60)

finally:
    db.close()
