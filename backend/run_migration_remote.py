#!/usr/bin/env python3
"""
Run production migration remotely via API
This adds ward, last_login, login_count columns to users table
"""
import requests
import sys

BASE_URL = "https://smartbursary-backend.onrender.com"

print("🔑 Logging in as admin...")
try:
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "admin@smartbursary.com",
            "password": "ChangeMe123!"
        },
        timeout=30
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        sys.exit(1)
    
    token = login_response.json()["token"]
    print("✅ Login successful!")
    
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("Make sure the backend is deployed and running")
    sys.exit(1)

print("\n🔧 Running production migration...")
print("This will add ward, last_login, and login_count columns to users table")

try:
    # Call a migration endpoint if it exists, or use setup endpoint
    response = requests.get(
        f"{BASE_URL}/api/setup/run-migration",
        headers={"Authorization": f"Bearer {token}"},
        timeout=60
    )
    
    if response.status_code == 404:
        print("⚠️  Migration endpoint not found")
        print("You need to run the migration manually via Render Shell:")
        print("  1. Go to Render Dashboard → Your Service → Shell")
        print("  2. Run: python run_production_migration.py")
    elif response.status_code == 200:
        print("✅ Migration completed successfully!")
        print(response.json())
    else:
        print(f"❌ Migration failed: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📝 Manual migration required:")
    print("  1. Go to Render Dashboard → Your Service → Shell")
    print("  2. Run: python run_production_migration.py")

print("\n" + "="*60)
print("Next steps:")
print("1. Verify CORS_ORIGINS is set on Render")
print("2. Test login at https://smart-bursary.vercel.app/")
print("="*60)
