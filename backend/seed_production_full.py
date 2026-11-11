"""
Seed production database with comprehensive demo data via API
This creates realistic test data for presentation
"""
import requests
import json
from datetime import datetime, timedelta, date
import random
import time

# Production API URL
BASE_URL = "https://smartbursary-backend.onrender.com/api"

# Admin credentials
ADMIN_EMAIL = "admin@smartbursary.com"
ADMIN_PASSWORD = "ChangeMe!"

# Sample data
FIRST_NAMES = ["John", "Mary", "Peter", "Grace", "David", "Faith", "James", "Lucy", "Daniel", "Rose", 
               "Samuel", "Elizabeth", "Joseph", "Catherine", "Michael", "Ann", "William", "Margaret"]
LAST_NAMES = ["Kamau", "Wanjiku", "Omondi", "Akinyi", "Kipchoge", "Chepkoech", "Mwangi", "Njeri", 
              "Otieno", "Adhiambo", "Ochieng", "Atieno", "Muriuki", "Wairimu", "Onyango", "Auma"]
WARDS = ["Central Ward", "East Ward", "West Ward", "North Ward", "South Ward"]
INSTITUTIONS = ["University of Nairobi", "Kenyatta University", "Moi University", "JKUAT", 
                "Strathmore University", "Maseno University", "Egerton University", "Technical University of Mombasa"]
COURSES = ["Computer Science", "Engineering", "Medicine", "Business Administration", "Education",
           "Law", "Agriculture", "Nursing", "Architecture", "Economics"]

def get_admin_token():
    """Login as admin and get token"""
    print("🔐 Logging in as admin...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
            timeout=30
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Admin login successful")
            return token
        else:
            print(f"❌ Admin login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return None

def get_bursaries(admin_token):
    """Get list of all bursaries"""
    print("\n📋 Fetching bursaries...")
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/bursaries", headers=headers, timeout=30)
        
        if response.status_code == 200:
            bursaries = response.json()
            print(f"✅ Found {len(bursaries)} bursaries")
            return bursaries
        else:
            print(f"❌ Failed to fetch bursaries: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error fetching bursaries: {e}")
        return []

def create_user(email, password, full_name, role, constituency, id_number, phone):
    """Create a user account via registration"""
    try:
        register_data = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "id_number": id_number,
            "phone_number": phone,
            "constituency": constituency,
            "ward": random.choice(WARDS)
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data, timeout=30)
        
        # Check various success scenarios
        if response.status_code == 200:
            return True, email
        elif "already exists" in response.text.lower() or "Registration successful" in response.text:
            return True, email
        else:
            return False, f"Registration failed: {response.status_code}"
    except Exception as e:
        return False, str(e)
def complete_profile(token, profile_data):
    """Complete user profile after registration"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Add required document flags and fields
        profile_data["has_national_id_doc"] = True
        profile_data["has_student_id_doc"] = True
        profile_data["county"] = "Nairobi"
        profile_data["sub_county"] = "N/A"
        profile_data["address"] = "Kenya"
        profile_data["guardian_name"] = "Guardian Name"
        profile_data["guardian_phone"] = "0700000000"
        profile_data["guardian_relationship"] = "Parent"
        profile_data["admission_year"] = 2022
        
        response = requests.patch(
            f"{BASE_URL}/profile",
            headers=headers,
            json=profile_data,
            timeout=30
        )
        return response.status_code == 200
    except Exception as e:
        return False
        return False

def submit_application_as_user(email, password, bursary_id, profile_data):
    """Login as user, complete profile, and submit application"""
    try:
        # 1. Login
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=30
        )
        
        if login_response.status_code != 200:
            return False, "Login failed"
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Complete profile
        complete_profile(token, profile_data)
        
        # 3. Submit application
        application_data = {
            "bursary_id": bursary_id,
            "institution": profile_data["institution"],
            "student_number": profile_data["student_number"],
            "national_id": profile_data["national_id"],
            "monthly_household_income": profile_data["monthly_household_income"],
            "household_size": profile_data["household_size"],
            "course": profile_data["course"],
            "year_of_study": profile_data["year_of_study"],
            "reason": "I am in need of financial assistance to continue my education. My family faces financial constraints and I require support to pursue my academic goals and contribute to society."
        }
        
        response = requests.post(
            f"{BASE_URL}/applications",
            headers=headers,
            json=application_data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            app_data = response.json()
            return True, app_data.get("application_number", "Unknown")
        else:
            return False, f"Application failed: {response.status_code} - {response.text[:200]}"
            
    except Exception as e:
        return False, str(e)

def promote_to_reviewer(email):
    """Promote user to reviewer role using setup endpoint"""
    try:
        response = requests.get(
            f"https://smartbursary-backend.onrender.com/api/setup/promote-reviewer?email={email}",
            timeout=30
        )
        return response.status_code == 200
    except:
        return False

def main():
    print("=" * 70)
    print("🚀 SmartBursary Production Full Demo Data Seeder")
    print("=" * 70)
    
    # Step 1: Login as admin
    admin_token = get_admin_token()
    if not admin_token:
        print("\n❌ Cannot proceed without admin access")
        return
    
    # Step 2: Get all bursaries
    bursaries = get_bursaries(admin_token)
    if not bursaries:
        print("\n⚠️ No bursaries found. Run constituency seeding first.")
        return
    
    # Get unique constituencies from bursaries
    constituencies = list(set([b.get("constituency") for b in bursaries if b.get("constituency")]))
    print(f"\n🗺️  Found {len(constituencies)} constituencies")
    
    # Step 3: Create reviewer accounts (5 from different constituencies)
    print("\n" + "=" * 70)
    print("👥 Creating Reviewer Accounts")
    print("=" * 70)
    
    reviewer_constituencies = random.sample(constituencies, min(5, len(constituencies)))
    reviewers_created = []
    
    for i, constituency in enumerate(reviewer_constituencies, 1):
        email = f"reviewer{i}@smartbursary.com"
        success, msg = create_user(
            email=email,
            password="reviewer123",
            full_name=f"{constituency} Reviewer",
            role="applicant",  # Register as applicant first
            constituency=constituency,
            id_number=f"1234567{i}",
            phone=f"0712{str(i).zfill(6)}"
        )
        
        if success:
            # Promote to reviewer
            if promote_to_reviewer(email):
                reviewers_created.append({"email": email, "constituency": constituency})
                print(f"  ✅ Created reviewer: {email} ({constituency})")
            else:
                print(f"  ⚠️ Created {email} but promotion failed")
        else:
            print(f"  ⚠️ {msg}")
        
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n✅ Created {len(reviewers_created)} reviewers")
    
    # Step 4: Create applicants and applications
    print("\n" + "=" * 70)
    print("👨‍🎓 Creating Applicants and Applications")
    print("=" * 70)
    
    # Select constituencies to create applicants for (use up to 10 constituencies for demo)
    selected_constituencies = random.sample(constituencies, min(10, len(constituencies)))
    
    applicants_created = 0
    applications_created = 0
    
    for constituency in selected_constituencies:
        # Get bursaries for this constituency
        constituency_bursaries = [b for b in bursaries if b.get("constituency") == constituency and b.get("active")]
        if not constituency_bursaries:
            continue
        
        # Create 2-3 applicants per constituency
        num_applicants = random.randint(2, 3)
        
        for j in range(num_applicants):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = f"{first_name.lower()}.{last_name.lower()}.{applicants_created}@student.ke"
            
            # Create user
            id_num = f"{random.randint(30000000, 39999999)}"
            phone = f"07{random.randint(10000000, 99999999)}"
            
            success, msg = create_user(
                email=email,
                password="student123",
                full_name=f"{first_name} {last_name}",
                role="applicant",
                constituency=constituency,
                id_number=id_num,
                phone=phone
            )
            
            if not success:
                print(f"  ⚠️ Failed to create {email}")
                continue
            
            applicants_created += 1
            
            # Prepare profile data
            profile_data = {
                "institution": random.choice(INSTITUTIONS),
                "student_number": f"S20/{random.randint(10000, 99999)}/2023",
                "course": random.choice(COURSES),
                "year_of_study": f"Year {random.randint(1, 4)}",
                "national_id": id_num,
                "monthly_household_income": random.randint(5000, 50000),
                "household_size": random.randint(2, 8),
                "date_of_birth": f"{2000 + random.randint(0, 5)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "gender": random.choice(["Male", "Female"])
            }
            
            # Submit 1-2 applications
            num_apps = random.randint(1, min(2, len(constituency_bursaries)))
            for bursary in random.sample(constituency_bursaries, num_apps):
                success, result = submit_application_as_user(
                    email=email,
                    password="student123",
                    bursary_id=bursary["id"],
                    profile_data=profile_data
                )
                
                if success:
                    applications_created += 1
                    print(f"  ✅ {email} → {bursary['name'][:40]}... (App: {result})")
                else:
                    print(f"  ⚠️ {email} application failed: {result[:100]}")
                
                time.sleep(0.3)  # Rate limiting
    
    print(f"\n✅ Created {applicants_created} applicants")
    print(f"✅ Created {applications_created} applications")
    
    # Step 5: Create main demo accounts if they don't exist
    print("\n" + "=" * 70)
    print("🔐 Creating Main Demo Accounts")
    print("=" * 70)
    
    # Main reviewer
    success, msg = create_user(
        email="reviewer@smartbursary.com",
        password="reviewer123",
        full_name="Demo Reviewer",
        role="applicant",
        constituency="Nairobi",
        id_number="12345678",
        phone="0712345678"
    )
    if success:
        promote_to_reviewer("reviewer@smartbursary.com")
        print("  ✅ Main reviewer: reviewer@smartbursary.com")
    
    # Main applicant
    success, msg = create_user(
        email="student@smartbursary.com",
        password="student123",
        full_name="Demo Student",
        role="applicant",
        constituency="Nairobi",
        id_number="87654321",
        phone="0787654321"
    )
    if success:
        print("  ✅ Main applicant: student@smartbursary.com")
    
    # Final Summary
    print("\n" + "=" * 70)
    print("✅ PRODUCTION SEEDING COMPLETE!")
    print("=" * 70)
    
    print("\n📊 Data Summary:")
    print(f"   • Total Bursaries: {len(bursaries)}")
    print(f"   • Constituencies: {len(constituencies)}")
    print(f"   • Reviewers Created: {len(reviewers_created)}")
    print(f"   • Applicants Created: {applicants_created}")
    print(f"   • Applications Created: {applications_created}")
    
    print("\n🔐 Main Demo Accounts:")
    print("   Admin:     admin@smartbursary.com / ChangeMe!")
    print("   Reviewer:  reviewer@smartbursary.com / reviewer123")
    print("   Student:   student@smartbursary.com / student123")
    
    print("\n📋 Additional Reviewers:")
    for r in reviewers_created[:3]:
        print(f"   • {r['email']} ({r['constituency']})")
    if len(reviewers_created) > 3:
        print(f"   ... and {len(reviewers_created) - 3} more")
    
    print("\n🌐 Production URL: https://smart-bursary.vercel.app/")
    print("=" * 70)
    print("\n🎉 Ready for presentation!")

if __name__ == "__main__":
    main()
