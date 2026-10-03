"""
Seed comprehensive test data for SmartBursary with real Kenya constituencies
Run this with: python seed_test_data.py
"""
import sys
import io

# Fix unicode output for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date, datetime, timedelta
from app.database import SessionLocal
from app.models import User, Bursary, Application, Document
from app.security import hash_password
from sqlalchemy import select
import json
import random

def seed_test_data():
    db = SessionLocal()
    
    try:
        print("🌱 Starting to seed test data...")
        
        # Define constituencies
        # Real Kenya constituencies with their counties
        constituencies_data = [
            {"constituency": "Westlands", "county": "Nairobi"},
            {"constituency": "Dagoretti North", "county": "Nairobi"},
            {"constituency": "Langata", "county": "Nairobi"},
            {"constituency": "Mvita", "county": "Mombasa"},
            {"constituency": "Kisauni", "county": "Mombasa"},
            {"constituency": "Kisumu East", "county": "Kisumu"},
            {"constituency": "Kisumu Central", "county": "Kisumu"},
            {"constituency": "Eldoret East", "county": "Uasin Gishu"},
            {"constituency": "Eldoret West", "county": "Uasin Gishu"},
            {"constituency": "Nakuru Town East", "county": "Nakuru"},
            {"constituency": "Nakuru Town West", "county": "Nakuru"},
            {"constituency": "Thika Town", "county": "Kiambu"},
            {"constituency": "Kikuyu", "county": "Kiambu"},
            {"constituency": "Starehe", "county": "Nairobi"},
            {"constituency": "Embakasi South", "county": "Nairobi"},
        ]
        
        constituencies = [c["constituency"] for c in constituencies_data]
        print(f"\n🗺️  Will create data for {len(constituencies)} constituencies across {len(set(c['county'] for c in constituencies_data))} counties")
        
        # 1. Create Bursaries for each constituency
        print("\n📋 Creating bursaries for each constituency...")
        bursaries_data = []
        for const_data in constituencies_data:
            constituency = const_data["constituency"]
            county = const_data["county"]
            # Create 2 bursaries per constituency
            bursary1 = Bursary(
                name=f"{constituency} CDF Bursary 2026",
                description=f"Constituency Development Fund bursary for students from {constituency}, {county} County.",
                eligibility=f"Must be a resident of {constituency} constituency in {county} County and enrolled in a recognized institution.",
                constituency=constituency,
                amount_kes=random.choice([15000, 20000, 25000, 30000]),
                show_amount=True,
                deadline=date.today() + timedelta(days=random.choice([30, 45, 60, 90])),
                required_documents=json.dumps([
                    "National ID or Birth Certificate",
                    "Admission Letter",
                    "Fee Structure",
                    "Parents ID Copies"
                ]),
                active=True
            )
            
            bursary2 = Bursary(
                name=f"{constituency} Merit Scholarship 2026",
                description=f"Merit-based scholarship for high-achieving students from {constituency} constituency, {county} County.",
                eligibility=f"Minimum B grade, resident of {constituency} constituency",
                constituency=constituency,
                amount_kes=random.choice([35000, 40000, 45000, 50000]),
                show_amount=random.choice([True, True, False]),
                deadline=date.today() + timedelta(days=random.choice([20, 40, 60])),
                required_documents=json.dumps([
                    "National ID",
                    "Academic Transcripts",
                    "Recommendation Letter",
                    "Fee Structure"
                ]),
                active=random.choice([True, True, True, False])  # 75% active
            )
            
            # Check if bursaries already exist
            existing1 = db.scalar(select(Bursary.id).where(Bursary.name == bursary1.name))
            existing2 = db.scalar(select(Bursary.id).where(Bursary.name == bursary2.name))
            
            if not existing1:
                db.add(bursary1)
                bursaries_data.append(bursary1)
                print(f"  ✓ Created: {bursary1.name}")
            
            if not existing2:
                db.add(bursary2)
                bursaries_data.append(bursary2)
                print(f"  ✓ Created: {bursary2.name}")
        
        db.commit()
        print(f"✅ Created {len(bursaries_data)} bursaries")
        
        # Refresh to get IDs
        for b in bursaries_data:
            db.refresh(b)
        
        # 2. Create Constituency Admins (one per constituency)
        print("\n👔 Creating constituency admins...")
        admins = []
        for const_data in constituencies_data:
            constituency = const_data["constituency"]
            county = const_data["county"]
            email = f"admin.{constituency.lower().replace(' ', '')}@smartbursary.com"
            existing = db.scalar(select(User.id).where(User.email == email))
            
            if not existing:
                admin = User(
                    full_name=f"{constituency} Admin",
                    email=email,
                    phone=f"0711{str(len(admins)+1).zfill(6)}",
                    password_hash=hash_password("admin123"),
                    role="admin",
                    constituency=constituency,
                    county=county,
                    profile_complete=True,
                    email_verified=True
                )
                db.add(admin)
                admins.append(admin)
                print(f"  ✓ Created: {email} ({constituency}, {county})")
        
        db.commit()
        print(f"✅ Created {len(admins)} constituency admins")
        
        # 3. Create Reviewers for each constituency
        print("\n👥 Creating reviewers for each constituency...")
        reviewers = []
        for const_data in constituencies_data:
            constituency = const_data["constituency"]
            county = const_data["county"]
            email = f"reviewer.{constituency.lower().replace(' ', '')}@smartbursary.com"
            existing = db.scalar(select(User.id).where(User.email == email))
            
            if not existing:
                reviewer = User(
                    full_name=f"{constituency} Reviewer",
                    email=email,
                    phone=f"0712{str(len(reviewers)+1).zfill(6)}",
                    password_hash=hash_password("reviewer123"),
                    role="reviewer",
                    constituency=constituency,
                    county=county,
                    profile_complete=True,
                    email_verified=True
                )
                db.add(reviewer)
                reviewers.append(reviewer)
                print(f"  ✓ Created: {email} ({constituency}, {county})")
        
        db.commit()
        print(f"✅ Created {len(reviewers)} reviewers")
        
        # 4. Create Test Applicants for each constituency
        print("\n👨‍🎓 Creating test applicants...")
        applicants = []
        first_names = ["John", "Mary", "Peter", "Grace", "David", "Sarah", "James", "Lucy"]
        last_names = ["Kamau", "Wanjiku", "Ochieng", "Atieno", "Kipchoge", "Mwangi", "Njeri", "Onyango"]
        
        for const_data in constituencies_data:
            constituency = const_data["constituency"]
            county = const_data["county"]
            # Create 3 applicants per constituency
            for j in range(3):
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                email = f"{fname.lower()}.{lname.lower()}.{len(applicants)}{j}@student.ke"
                
                existing = db.scalar(select(User.id).where(User.email == email))
                if existing:
                    continue
                
                applicant = User(
                    full_name=f"{fname} {lname}",
                    email=email,
                    phone=f"07{random.randint(10000000, 99999999)}",
                    password_hash=hash_password("student123"),
                    role="applicant",
                    constituency=constituency,
                    county=county,
                    profile_complete=True,
                    email_verified=True,
                    date_of_birth=date(2002 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    national_id=f"{random.randint(30000000, 39999999)}",
                    gender=random.choice(["Male", "Female"]),
                    institution=random.choice(["University of Nairobi", "Kenyatta University", "Moi University", "JKUAT", "Strathmore University"]),
                    student_number=f"STU{random.randint(100000, 999999)}",
                    course=random.choice(["Computer Science", "Business Administration", "Engineering", "Medicine", "Education"]),
                    year_of_study="Year " + str(random.randint(1, 4)),
                    monthly_household_income=random.randint(5000, 50000),
                    household_size=random.randint(2, 8)
                )
                db.add(applicant)
                applicants.append(applicant)
                print(f"  ✓ Created: {email} (constituency: {constituency})")
        
        db.commit()
        print(f"✅ Created {len(applicants)} test applicants")
        
        # Refresh to get IDs
        for a in applicants:
            db.refresh(a)
        
        # 4. Create Applications
        print("\n📝 Creating applications...")
        all_bursaries = db.scalars(select(Bursary)).all()
        statuses = [
            "Submitted",
            "Under Review",
            "Verification",
            "Committee Review",
            "Approved",
            "Approved",  # More approved for disbursement testing
            "Disbursed",
            "Rejected"
        ]
        
        applications_created = 0
        for applicant in applicants:
            # Each applicant applies to 1-2 bursaries from their constituency
            constituency_bursaries = [b for b in all_bursaries if b.constituency == applicant.constituency]
            num_applications = random.randint(1, min(2, len(constituency_bursaries)))
            
            for bursary in random.sample(constituency_bursaries, num_applications):
                # Check if application already exists
                existing = db.scalar(
                    select(Application.id).where(
                        Application.applicant_id == applicant.id,
                        Application.bursary_id == bursary.id
                    )
                )
                if existing:
                    continue
                
                count = db.scalar(select(func.count(Application.id))) or 0
                app_number = f"SB-2026-{count + applications_created + 1:05d}"
                
                # Ensure unique number
                while db.scalar(select(Application.id).where(Application.application_number == app_number)):
                    count += 1
                    app_number = f"SB-2026-{count + applications_created + 1:05d}"
                
                status = random.choice(statuses)
                submitted_date = datetime.now() - timedelta(days=random.randint(1, 30))
                
                # Calculate priority score
                income = applicant.monthly_household_income
                household = applicant.household_size
                priority_score = 50 + round((1 - min(income / 60000, 1)) * 35) + (8 if household > 4 else 0)
                priority_score = min(95, max(0, priority_score))
                
                application = Application(
                    application_number=app_number,
                    applicant_id=applicant.id,
                    bursary_id=bursary.id,
                    institution=applicant.institution,
                    student_number=applicant.student_number,
                    national_id=applicant.national_id,
                    monthly_household_income=applicant.monthly_household_income,
                    household_size=applicant.household_size,
                    course=applicant.course,
                    year_of_study=applicant.year_of_study,
                    reason=f"I am applying for this bursary to help me continue my studies in {applicant.course}. My family's financial situation makes it difficult to afford tuition fees.",
                    status=status,
                    priority_score=priority_score,
                    financial_need="HIGH" if income < 20000 else "MEDIUM",
                    education_need="MEDIUM",
                    duplicate_risk="LOW",
                    reviewer_comment="Reviewed by system" if status != "Submitted" else "",
                    submitted_at=submitted_date,
                    updated_at=datetime.now() if status != "Submitted" else submitted_date
                )
                db.add(application)
                applications_created += 1
        
        db.commit()
        print(f"✅ Created {applications_created} applications")
        
        print("\n" + "="*60)
        print("✅ Test data seeding completed successfully!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"   • Constituencies: {len(constituencies)}")
        print(f"   • Counties: {len(set(c['county'] for c in constituencies_data))}")
        print(f"   • Bursaries: {len(bursaries_data)}")
        print(f"   • Constituency Admins: {len(admins)}")
        print(f"   • Reviewers: {len(reviewers)}")
        print(f"   • Applicants: {len(applicants)}")
        print(f"   • Applications: {applications_created}")
        
        print("\n🔐 Login Credentials:")
        print("\n   Super Admin (optional - see all constituencies):")
        print("   Email: admin@smartbursary.com")
        print("   Password: admin123")
        
        print("\n   Constituency Admins (all use password: admin123):")
        for const_data in constituencies_data[:5]:  # Show first 5
            const = const_data["constituency"]
            county = const_data["county"]
            print(f"   • admin.{const.lower().replace(' ', '')}@smartbursary.com ({const}, {county})")
        if len(constituencies_data) > 5:
            print(f"   ... and {len(constituencies_data) - 5} more")
        
        print("\n   Reviewers (all use password: reviewer123):")
        for const_data in constituencies_data[:5]:  # Show first 5
            const = const_data["constituency"]
            print(f"   • reviewer.{const.lower().replace(' ', '')}@smartbursary.com ({const})")
        if len(constituencies_data) > 5:
            print(f"   ... and {len(constituencies_data) - 5} more")
        
        print("\n   Applicants (all use password: student123):")
        for applicant in applicants[:3]:  # Show first 3
            print(f"   • {applicant.email}")
        print("   ... and more")
        
        print("\n🎉 Ready to test!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Import func here to avoid issues
    from sqlalchemy import func
    seed_test_data()
