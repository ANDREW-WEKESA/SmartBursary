"""
SMS notification service using Africa's Talking API
Sends SMS for registration, application submission, and status updates
"""
import os
import requests
from typing import Optional

class SMSService:
    def __init__(self):
        self.username = os.getenv("AFRICASTALKING_USERNAME", "sandbox")
        self.api_key = os.getenv("AFRICASTALKING_API_KEY", "")
        self.sender_id = os.getenv("SMS_SENDER_ID", "SmartBursary")
        self.enabled = os.getenv("SMS_ENABLED", "false").lower() == "true"
        
        # Use sandbox or production URL
        if self.username == "sandbox":
            self.base_url = "https://api.sandbox.africastalking.com/version1"
        else:
            self.base_url = "https://api.africastalking.com/version1"
    
    def send_sms(self, phone: str, message: str) -> bool:
        """
        Send SMS to a phone number
        
        Args:
            phone: Phone number in format +254XXXXXXXXX
            message: SMS message content
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[SMS] SMS disabled. Would send to {phone}: {message}")
            return False
        
        if not self.api_key:
            print("[SMS] Africa's Talking API key not configured")
            return False
        
        # Ensure phone number starts with +254
        if phone.startswith("0"):
            phone = "+254" + phone[1:]
        elif not phone.startswith("+"):
            phone = "+" + phone
        
        try:
            url = f"{self.base_url}/messaging"
            headers = {
                "apiKey": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            data = {
                "username": self.username,
                "to": phone,
                "message": message,
                "from": self.sender_id
            }
            
            print(f"[SMS] Sending SMS to {phone}")
            response = requests.post(url, headers=headers, data=data, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                print(f"[SMS] Response: {result}")
                
                # Check if message was accepted
                if result.get("SMSMessageData", {}).get("Recipients"):
                    recipients = result["SMSMessageData"]["Recipients"]
                    if recipients and recipients[0].get("status") == "Success":
                        print(f"[SMS] ✓ SMS sent successfully to {phone}")
                        return True
                    else:
                        print(f"[SMS] ✗ SMS failed: {recipients[0].get('status')}")
                        return False
                else:
                    print(f"[SMS] ✗ No recipients in response")
                    return False
            else:
                print(f"[SMS] ✗ HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"[SMS] ✗ Error sending SMS: {str(e)}")
            return False
    
    def send_registration_sms(self, phone: str, full_name: str, otp: str) -> bool:
        """Send welcome SMS with OTP after registration"""
        message = (
            f"Welcome to SmartBursary, {full_name}! "
            f"Your verification code is: {otp}. "
            f"Valid for 10 minutes. Do not share this code."
        )
        return self.send_sms(phone, message)
    
    def send_application_submitted_sms(self, phone: str, full_name: str, application_number: str, bursary_name: str) -> bool:
        """Send confirmation SMS when application is submitted"""
        message = (
            f"Dear {full_name}, your bursary application ({application_number}) "
            f"for {bursary_name} has been received. "
            f"Track your application at smart-bursary.vercel.app"
        )
        return self.send_sms(phone, message)
    
    def send_status_change_sms(self, phone: str, full_name: str, application_number: str, new_status: str) -> bool:
        """Send SMS when application status changes"""
        
        # Different messages for different statuses
        status_messages = {
            "Under Review": f"Dear {full_name}, your application {application_number} is now under review. We'll notify you of any updates.",
            "Verification": f"Dear {full_name}, your application {application_number} is in verification stage. Please ensure all documents are uploaded.",
            "Additional Information Required": f"Dear {full_name}, your application {application_number} requires additional information. Please check your dashboard.",
            "Committee Review": f"Dear {full_name}, your application {application_number} is with the awards committee for final review.",
            "Approved": f"Congratulations {full_name}! Your bursary application {application_number} has been APPROVED. Disbursement details will follow soon.",
            "Rejected": f"Dear {full_name}, we regret to inform you that application {application_number} was not successful this time. You may apply again in future.",
            "Disbursed": f"Great news {full_name}! Your bursary funds for application {application_number} have been DISBURSED. Check your payment details in the dashboard."
        }
        
        message = status_messages.get(new_status, f"Dear {full_name}, your application {application_number} status changed to: {new_status}")
        return self.send_sms(phone, message)
    
    def send_password_reset_sms(self, phone: str, full_name: str, otp: str) -> bool:
        """Send SMS with password reset OTP"""
        message = (
            f"Hi {full_name}, your SmartBursary password reset code is: {otp}. "
            f"Valid for 10 minutes. If you didn't request this, ignore this message."
        )
        return self.send_sms(phone, message)


# Global SMS service instance
sms_service = SMSService()
