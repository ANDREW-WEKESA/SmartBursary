import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "andrewwekesa675@gmail.com"
SMTP_PASSWORD = "kgmvqwsmpqpihivd"
SMTP_FROM_EMAIL = "andrewwekesa675@gmail.com"

def test_email():
    try:
        print("Testing SMTP connection...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test Email from SmartBursary"
        msg['From'] = f"SmartBursary <{SMTP_FROM_EMAIL}>"
        msg['To'] = SMTP_USERNAME
        
        html_body = """
        <html>
        <body>
            <h2>Test Email</h2>
            <p>If you receive this, your email configuration is working!</p>
            <p>Your OTP code would be: <strong>123456</strong></p>
        </body>
        </html>
        """
        
        part = MIMEText(html_body, 'html')
        msg.attach(part)
        
        # Connect and send
        print(f"Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            print("Starting TLS...")
            server.starttls()
            
            print(f"Logging in as {SMTP_USERNAME}...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            
            print("Sending email...")
            server.send_message(msg)
            
        print("✅ SUCCESS! Email sent successfully!")
        print(f"Check your inbox: {SMTP_USERNAME}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}")
        print(f"Details: {str(e)}")
        return False

if __name__ == "__main__":
    test_email()
