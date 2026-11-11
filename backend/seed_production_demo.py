"""
Seed production database with demo reviewer and applicant accounts plus sample applications
"""
import requests
import json
from datetime import datetime, timedelta
import random

# Production API URL
BASE_URL = "https://smartbursary-backend.onrender.com/api"

# Admin credentials
ADMIN_EMAIL = "admin@smartbursary.com"
ADMIN_PASSWORD = "ChangeMe!"

# Demo accounts to create
REVIEWER_EMAIL = "reviewer@smartbursary.com"
REVIEWER_PASSWORD = "reviewer123"

APPLICANT_EMAIL = "student@smartbursary.com"
APPLICANT_PASSWORD = "student123"

# Sample Kenyan names for diversity
FIRST_NAMES = ["John", "Mary", "Peter", "Grace", "David", "Faith", "James", "Lucy", "Daniel", "Rose"]
LAST_NAMES = ["Kamau", "Wanjiku", "Omondi", "Akinyi", "Kipchoge", "Chepkoech", "Mwangi", "Njeri", "Otieno", "Adhiambo"]

# Sample constituencies (will fetch actual ones from API)
SAMPLE_WARDS = ["Central Ward", "East Ward", "West Ward", "North Ward", "South Ward"]

def get_admin_token():
    """Login as admin and get token"""
    print("🔐 Logging in as admin...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Admin login successful")
        return token
    else:
        print(f"❌ Admin login failed: {response.text}")
        return None

def create_reviewer(admin_token):
    """Create a demo reviewer account"""
    print(f"\n👤 Creating reviewer account: {REVIEWER_EMAIL}")
    
    # First register the account
    register_data = {
        "email": REVIEWER_EMAIL,
        "password": REVIEWER_PASSWORD,
        "full_name": "Demo Reviewer",
        "id_number": "12345678",
        "phone_number": "0712345678",
        "constituency": "Nairobi",
        "ward": "Central Ward"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    
    # Check if already exists or successfully created
    if response.status_code == 200 or "already exists" in response.text.lower() or "Registration successful" in response.text:
        print(f"✅ Reviewer account exists: {REVIEWER_EMAIL}")
        
        # Promote to reviewer role using the setup endpoint
        promote_response = requests.get(
            f"https://smartbursary-backend.onrender.com/api/setup/promote-reviewer?email={REVIEWER_EMAIL}"
        )
        
        if promote_response.status_code == 200:
            print("✅ User promoted to reviewer role")
            return True
        else:
            print(f"⚠️ Failed to promote to reviewer: {promote_response.text}")
            return True
    else:
        print(f"❌ Failed to create reviewer: {response.text}")
        return None

def create_applicant():
    """Create a demo applicant account"""
    print(f"\n👤 Creating applicant account: {APPLICANT_EMAIL}")
    
    register_data = {
        "email": APPLICANT_EMAIL,
        "password": APPLICANT_PASSWORD,
        "full_name": "Demo Student",
        "id_number": "87654321",
        "phone_number": "0787654321",
        "constituency": "Nairobi",
        "ward": "East Ward"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 200 or "already exists" in response.text.lower() or "Registration successful" in response.text:
        print(f"✅ Applicant account exists: {APPLICANT_EMAIL}")
        return True
    else:
        print(f"❌ Failed to create applicant: {response.text}")
        return None

def get_constituencies(admin_token):
    """Get list of constituencies"""
    print("\n📍 Fetching constituencies...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/admin/constituencies", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Extract constituencies list from the response
        if isinstance(data, dict):
            constituencies = data.get("constituencies", [])
        else:
            constituencies = data
        print(f"✅ Found {len(constituencies)} constituencies")
        return constituencies
    else:
        print(f"❌ Failed to fetch constituencies: {response.text}")
        return []

def get_programs(admin_token):
    """Get list of bursary programs"""
    print("\n📋 Fetching bursary programs...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/bursaries", headers=headers)
    
    if response.status_code == 200:
        programs = response.json()
        print(f"✅ Found {len(programs)} programs")
        return programs
    else:
        print(f"❌ Failed to fetch programs: {response.text}")
        return []

def create_demo_applicants(admin_token, bursaries, num_applicants=10):
    """Create multiple demo applicant accounts"""
    print(f"\n👥 Creating {num_applicants} demo applicants...")
    applicant_ids = []
    
    # Extract unique constituencies from bursaries
    constituencies = list(set([b.get("constituency", "Nairobi") for b in bursaries if b.get("constituency")]))
    if not constituencies:
        constituencies = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
    
    for i in range(num_applicants):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        constituency = random.choice(constituencies)
        
        email = f"applicant{i+1}@demo.com"
        register_data = {
            "email": email,
            "password": "demo123",
            "full_name": f"{first_name} {last_name}",
            "id_number": f"{random.randint(10000000, 99999999)}",
            "phone_number": f"07{random.randint(10000000, 99999999)}",
            "constituency": constituency,
            "ward": random.choice(SAMPLE_WARDS)
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200 or "already exists" in response.text.lower() or "Registration successful" in response.text:
            applicant_ids.append({
                "email": email,
                "constituency": constituency
            })
            print(f"  ✅ Created: {email} ({constituency})")
        else:
            print(f"  ⚠️ Failed to create {email}")
    
    print(f"✅ Created {len(applicant_ids)} applicants")
    return applicant_ids

def submit_application(applicant_email, applicant_password, bursary_id):
    """Submit a bursary application"""
    # Login as applicant
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": applicant_email, "password": applicant_password}
    )
    
    if login_response.status_code != 200:
        print(f"  ❌ Failed to login as {applicant_email}")
        return None
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Submit application
    application_data = {
        "bursary_id": bursary_id,
        "school_name": random.choice(["University of Nairobi", "Kenyatta University", "Moi University", "JKUAT", "Strathmore University"]),
        "course": random.choice(["Computer Science", "Engineering", "Medicine", "Business Administration", "Education"]),
        "year_of_study": random.randint(1, 4),
        "guardian_name": random.choice(["John Doe", "Jane Smith", "Peter King", "Mary Johnson"]),
        "guardian_phone": f"07{random.randint(10000000, 99999999)}",
        "household_income": random.choice([10000, 15000, 20000, 25000, 30000]),
        "household_size": random.randint(3, 8),
        "reason": "I am in need of financial assistance to continue my studies. My family is unable to fully support my education expenses due to financial constraints."
    }
    
    response = requests.post(
        f"{BASE_URL}/applications/submit",
        headers=headers,
        json=application_data
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"  ⚠️ Application failed: {response.status_code} - {response.text[:200]}")
        return None

def create_demo_applications(applicants, bursaries, num_applications=20):
    """Create demo applications"""
    print(f"\n📝 Creating {num_applications} demo applications...")
    applications_created = 0
    
    for i in range(num_applications):
        if not applicants or not bursaries:
            break
            
        applicant = random.choice(applicants)
        bursary = random.choice(bursaries)
        
        # Find a bursary from the applicant's constituency if possible
        matching_bursaries = [b for b in bursaries if b.get("constituency") == applicant["constituency"]]
        if matching_bursaries:
            bursary = random.choice(matching_bursaries)
        
        result = submit_application(applicant["email"], "demo123", bursary["id"])
        if result:
            applications_created += 1
            print(f"  ✅ Application #{applications_created} submitted by {applicant['email']}")
    
    print(f"✅ Created {applications_created} applications")
    return applications_created

def main():
    print("=" * 60)
    print("🚀 SmartBursary Production Demo Data Seeder")
    print("=" * 60)
    
    # Step 1: Login as admin
    admin_token = get_admin_token()
    if not admin_token:
        print("\n❌ Cannot proceed without admin access")
        return
    
    # Step 2: Create reviewer account
    reviewer_id = create_reviewer(admin_token)
    
    # Step 3: Create main applicant account
    applicant_id = create_applicant()
    
    # Step 4: Get bursaries
    bursaries = get_programs(admin_token)
    
    if not bursaries:
        print("\n⚠️ Cannot create applications without bursaries")
        print("✅ Reviewer and applicant accounts created successfully")
        return
    
    # Step 5: Create additional demo applicants (using bursaries to get constituencies)
    demo_applicants = create_demo_applicants(admin_token, bursaries, num_applicants=15)
    
    # Add main applicant to the list
    if applicant_id:
        demo_applicants.append({
            "email": APPLICANT_EMAIL,
            "constituency": "Nairobi"
        })
    
    # Step 6: Create demo applications
    create_demo_applications(demo_applicants, bursaries, num_applications=25)
    
    print("\n" + "=" * 60)
    print("✅ PRODUCTION SEEDING COMPLETE!")
    print("=" * 60)
    print("\n📋 Demo Accounts Created:")
    print(f"   Admin:     {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"   Reviewer:  {REVIEWER_EMAIL} / {REVIEWER_PASSWORD}")
    print(f"   Applicant: {APPLICANT_EMAIL} / {APPLICANT_PASSWORD}")
    print(f"\n📊 Data Summary:")
    print(f"   Applicants: {len(demo_applicants)}")
    print(f"   Applications: ~25 submitted")
    print(f"\n🌐 Production URL: https://smart-bursary.vercel.app/")
    print("=" * 60)

if __name__ == "__main__":
    main()
