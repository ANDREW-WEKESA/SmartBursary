"""Activate andrewwekesa675@gmail.com account via API"""
import requests

# Use the production API
base_url = "https://smartbursary-backend.onrender.com"

# First, let's use forgot password to enable the account
# This will set active=True when you reset the password
email = "andrewwekesa675@gmail.com"

print(f"Requesting password reset for {email}...")
response = requests.post(
    f"{base_url}/api/auth/forgot-password",
    json={"email": email}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print("\nCheck your email for the OTP code, then use it to reset your password!")
print("This will also activate your account.")
