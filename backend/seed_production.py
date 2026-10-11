#!/usr/bin/env python3
"""
Script to seed the production database via API endpoint
"""
import requests
import json

# Production backend URL
BASE_URL = "https://smartbursary-backend.onrender.com"

print("🔑 Logging in as super admin...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": "admin@smartbursary.com",
        "password": "ChangeMe123!"
    }
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()["token"]
print("✅ Login successful!")

print("\n🌱 Seeding production database...")
seed_response = requests.post(
    f"{BASE_URL}/api/admin/seed-database",
    headers={"Authorization": f"Bearer {token}"}
)

if seed_response.status_code != 200:
    print(f"❌ Seeding failed: {seed_response.status_code}")
    print(seed_response.text)
    exit(1)

result = seed_response.json()
print("✅ Seeding successful!")
print("\n📊 Summary:")
print(json.dumps(result, indent=2))
