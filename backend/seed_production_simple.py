"""
Simple production seeder - creates reviewers and applicant accounts only
Applications can be created manually during demo
"""
import requests
import random
import time

BASE_URL = "https://smartbursary-backend.onrender.com/api"
ADMIN_EMAIL = "admin@smartbursary.com"
ADMIN_PASSWORD = "ChangeMe!"

FIRST_NAMES = ["John", "Mary", "Peter", "Grace", "David", "Faith", "James", "Lucy", "Daniel", "Rose"]
LAST_NAMES = ["Kamau", "Wanjiku", "Omondi", "Akinyi", "Kipchoge", "Chepkoech", "Mwangi", "Njeri", "Otieno", "Adhiambo"]
WARDS = ["Central Ward", "East Ward", "West Ward", "North Ward", "South Ward"]

def get_admin_token():
    print("🔐 Logging in as admin...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=30
    )
    if response.status_code == 200:
        print("✅ Admin login successful")
        return response.json()["access_token"]
    return None

def get_bursaries(admin_token):
    print("\n📋 Fetching bursaries...")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/bursaries", headers=headers, timeout=30)
    if response.status_code == 200:
        bursaries = response.json()
        print(f"✅ Found {len(bursaries)} bursaries")
        return bursaries
    return []

def create_user(email, password, full_name, constituency, id_number, phone):
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
        return response.status_code == 200 or "Registration successful" in response.text or "already exists" in response.text.lower()
    except:
        return False

def promote_to_reviewer(email):
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
    print("🚀 SmartBursary Production Simple Seeder")
    print("=" * 70)
    
    admin_token = get_admin_token()
    if not admin_token:
        return
    
    bursaries = get_bursaries(admin_token)
    if not bursaries:
        return
    
    constituencies = list(set([b.get("constituency") for b in bursaries if b.get("constituency")]))
    print(f"\n🗺️  Found {len(constituencies)} constituencies")
    
    # Create 5 reviewers
    print("\n" + "=" * 70)
    print("👥 Creating Reviewers")
    print("=" * 70)
    
    reviewer_constituencies = random.sample(constituencies, min(5, len(constituencies)))
    reviewers_created = 0
    
    for i, constituency in enumerate(reviewer_constituencies, 1):
        email = f"reviewer{i}@smartbursary.com"
        if create_user(email, "reviewer123", f"{constituency} Reviewer", constituency, f"1234567{i}", f"0712{str(i).zfill(6)}"):
            if promote_to_reviewer(email):
                reviewers_created += 1
                print(f"  ✅ {email} ({constituency})")
        time.sleep(0.3)
    
    print(f"\n✅ Created {reviewers_created} reviewers")
    
    # Create applicants (no applications)
    print("\n" + "=" * 70)
    print("👨‍🎓 Creating Applicants")
    print("=" * 70)
    
    selected_constituencies = random.sample(constituencies, min(10, len(constituencies)))
    applicants_created = 0
    
    for constituency in selected_constituencies:
        for j in range(2):  # 2 per constituency = 20 total
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            email = f"{first_name.lower()}.{last_name.lower()}.{applicants_created}@student.ke"
            
            if create_user(email, "student123", f"{first_name} {last_name}", constituency, f"{random.randint(30000000, 39999999)}", f"07{random.randint(10000000, 99999999)}"):
                applicants_created += 1
                print(f"  ✅ {email} ({constituency})")
            
            time.sleep(0.2)
    
    print(f"\n✅ Created {applicants_created} applicants")
    
    # Ensure main demo accounts exist
    print("\n" + "=" * 70)
    print("🔐 Creating Main Demo Accounts")
    print("=" * 70)
    
    if create_user("reviewer@smartbursary.com", "reviewer123", "Demo Reviewer", "Nairobi", "12345678", "0712345678"):
        promote_to_reviewer("reviewer@smartbursary.com")
        print("  ✅ reviewer@smartbursary.com")
    
    if create_user("student@smartbursary.com", "student123", "Demo Student", "Nairobi", "87654321", "0787654321"):
        print("  ✅ student@smartbursary.com")
    
    print("\n" + "=" * 70)
    print("✅ PRODUCTION SEEDING COMPLETE!")
    print("=" * 70)
    
    print("\n📊 Summary:")
    print(f"   • Bursaries: {len(bursaries)} (290 constituencies)")
    print(f"   • Reviewers: {reviewers_created}")
    print(f"   • Applicants: {applicants_created}")
    
    print("\n🔐 Main Accounts:")
    print("   Admin:    admin@smartbursary.com / ChangeMe!")
    print("   Reviewer: reviewer@smartbursary.com / reviewer123")
    print("   Student:  student@smartbursary.com / student123")
    
    print("\n💡 Next Steps:")
    print("   1. Login to https://smart-bursary.vercel.app/")
    print("   2. Use applicant accounts to complete profiles and submit applications")
    print("   3. Use reviewer accounts to review applications")
    print("   4. Use admin account for full system access")
    
    print("\n🎉 Ready for demo!")

if __name__ == "__main__":
    main()
