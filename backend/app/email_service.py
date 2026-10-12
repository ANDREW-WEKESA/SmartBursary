import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging
import random
import requests
from .config import settings

logger = logging.getLogger(__name__)


def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_email_via_sendgrid_api(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Send email using SendGrid HTTP API (works on Render free tier)."""
    try:
        logger.info(f"Sending email to {to_email} via SendGrid HTTP API")
        
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {
            "Authorization": f"Bearer {settings.smtp_password}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "personalizations": [{
                "to": [{"email": to_email}],
                "subject": subject
            }],
            "from": {
                "email": settings.smtp_from_email,
                "name": settings.smtp_from_name
            },
            "content": [
                {"type": "text/plain", "value": text_body or ""},
                {"type": "text/html", "value": html_body}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 202:
            logger.info(f"Email sent successfully to {to_email} via SendGrid API")
            return True
        else:
            logger.error(f"SendGrid API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Failed to send email via SendGrid API: {type(e).__name__}: {str(e)}")
        logger.exception(e)
        return False


def send_email(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Send an email using SendGrid HTTP API or SMTP."""
    logger.info(f"Email config: enabled={settings.email_enabled}, host={settings.smtp_host}, port={settings.smtp_port}, user={settings.smtp_username}")
    
    if not settings.email_enabled:
        logger.info(f"Email disabled. Would have sent to {to_email}: {subject}")
        return False
    
    # If using SendGrid, use HTTP API instead of SMTP (Render blocks SMTP ports)
    if settings.smtp_host == "smtp.sendgrid.net" and settings.smtp_username == "apikey":
        return send_email_via_sendgrid_api(to_email, subject, html_body, text_body)
    
    try:
        logger.info(f"Attempting to send email to {to_email} via {settings.smtp_host}")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
        msg['To'] = to_email
        
        # Add plain text version if provided, otherwise strip HTML
        if text_body:
            part1 = MIMEText(text_body, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)
        
        # Connect to SMTP server with shorter timeout
        try:
            if settings.smtp_port == 465:
                # SSL
                logger.info(f"Connecting via SSL to {settings.smtp_host}:{settings.smtp_port}")
                with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    logger.info("SSL connection established, logging in...")
                    if settings.smtp_username:
                        server.login(settings.smtp_username, settings.smtp_password)
                    logger.info("Login successful, sending message...")
                    server.send_message(msg)
            else:
                # TLS or plain
                logger.info(f"Connecting via TLS to {settings.smtp_host}:{settings.smtp_port}")
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
                    if settings.smtp_port == 587:
                        logger.info("Starting TLS...")
                        server.starttls()
                    if settings.smtp_username:
                        logger.info("Logging in...")
                        server.login(settings.smtp_username, settings.smtp_password)
                    logger.info("Sending message...")
                    server.send_message(msg)
        except OSError as e:
            if e.errno == 101:  # Network unreachable
                logger.error(f"Network unreachable. Render free tier blocks external SMTP. Use SendGrid instead.")
            raise
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            logger.error("Check your SMTP_USERNAME and SMTP_PASSWORD in Render environment variables")
            raise
        except Exception as e:
            logger.error(f"SMTP connection error: {type(e).__name__}: {str(e)}")
            raise
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {type(e).__name__}: {str(e)}")
        logger.exception(e)  # This will log the full traceback
        return False


def send_application_submitted_email(applicant_email: str, applicant_name: str, bursary_name: str, app_number: str):
    """Send email when application is submitted."""
    subject = "Application Submitted - SmartBursary"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Application Submitted Successfully</h2>
            <p>Dear {applicant_name},</p>
            <p>Your bursary application has been submitted successfully.</p>
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Application Number:</strong> {app_number}</p>
                <p style="margin: 5px 0;"><strong>Bursary:</strong> {bursary_name}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> Pending Review</p>
            </div>
            <p>Your application is now under review. You will receive an email notification once a decision has been made.</p>
            <p style="margin-top: 30px;">Best regards,<br>SmartBursary Team</p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
Application Submitted Successfully

Dear {applicant_name},

Your bursary application has been submitted successfully.

Application Number: {app_number}
Bursary: {bursary_name}
Status: Pending Review

Your application is now under review. You will receive an email notification once a decision has been made.

Best regards,
SmartBursary Team
    """
    
    send_email(applicant_email, subject, html_body, text_body)


def send_application_status_changed_email(applicant_email: str, applicant_name: str, bursary_name: str, app_number: str, new_status: str, amount: float = None):
    """Send email when application status changes."""
    status_messages = {
        "approved": {
            "subject": "Application Approved - SmartBursary",
            "title": "Congratulations! Your Application Has Been Approved",
            "message": "We are pleased to inform you that your bursary application has been approved.",
            "color": "#10b981"
        },
        "rejected": {
            "subject": "Application Update - SmartBursary",
            "title": "Application Status Update",
            "message": "After careful review, we regret to inform you that your bursary application was not approved at this time.",
            "color": "#ef4444"
        },
        "disbursed": {
            "subject": "Bursary Disbursed - SmartBursary",
            "title": "Your Bursary Has Been Disbursed",
            "message": "Your approved bursary funds have been disbursed.",
            "color": "#8b5cf6"
        }
    }
    
    status_info = status_messages.get(new_status.lower(), {
        "subject": "Application Status Update - SmartBursary",
        "title": "Application Status Update",
        "message": f"Your application status has been updated to: {new_status}",
        "color": "#6b7280"
    })
    
    amount_section = ""
    if amount and new_status.lower() in ["approved", "disbursed"]:
        amount_section = f'<p style="margin: 5px 0;"><strong>Amount:</strong> KES {amount:,.2f}</p>'
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: {status_info['color']};">{status_info['title']}</h2>
            <p>Dear {applicant_name},</p>
            <p>{status_info['message']}</p>
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Application Number:</strong> {app_number}</p>
                <p style="margin: 5px 0;"><strong>Bursary:</strong> {bursary_name}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> {new_status.title()}</p>
                {amount_section}
            </div>
            <p>If you have any questions, please contact your constituency office.</p>
            <p style="margin-top: 30px;">Best regards,<br>SmartBursary Team</p>
        </div>
    </body>
    </html>
    """
    
    amount_text = f"\nAmount: KES {amount:,.2f}" if amount and new_status.lower() in ["approved", "disbursed"] else ""
    
    text_body = f"""
{status_info['title']}

Dear {applicant_name},

{status_info['message']}

Application Number: {app_number}
Bursary: {bursary_name}
Status: {new_status.title()}{amount_text}

If you have any questions, please contact your constituency office.

Best regards,
SmartBursary Team
    """
    
    send_email(applicant_email, status_info['subject'], html_body, text_body)


def send_new_application_notification_to_reviewers(reviewer_emails: List[str], bursary_name: str, applicant_name: str, constituency: str, app_number: str):
    """Send notification to reviewers when a new application is submitted."""
    if not reviewer_emails:
        logger.warning(f"No reviewer emails provided for {constituency} constituency")
        return
    
    subject = f"New Application to Review - {constituency}"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">New Bursary Application for Review</h2>
            <p>A new bursary application has been submitted for your review.</p>
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Application Number:</strong> {app_number}</p>
                <p style="margin: 5px 0;"><strong>Bursary:</strong> {bursary_name}</p>
                <p style="margin: 5px 0;"><strong>Applicant:</strong> {applicant_name}</p>
                <p style="margin: 5px 0;"><strong>Constituency:</strong> {constituency}</p>
            </div>
            <p>Please log in to the SmartBursary system to review this application.</p>
            <p style="margin-top: 30px;">Best regards,<br>SmartBursary System</p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
New Bursary Application for Review

A new bursary application has been submitted for your review.

Application Number: {app_number}
Bursary: {bursary_name}
Applicant: {applicant_name}
Constituency: {constituency}

Please log in to the SmartBursary system to review this application.

Best regards,
SmartBursary System
    """
    
    for email in reviewer_emails:
        send_email(email, subject, html_body, text_body)


def send_otp_email(email: str, full_name: str, otp_code: str, purpose: str = "registration"):
    """Send OTP verification email for registration or password reset."""
    
    if purpose == "password_reset":
        subject = "Password Reset Code - SmartBursary"
        title = "Password Reset Request"
        message = "We received a request to reset your password. Use the code below to reset your password:"
        expiry_note = "If you didn't request a password reset, please ignore this email and your password will remain unchanged."
    else:
        subject = "Verify Your Email - SmartBursary"
        title = "Email Verification"
        message = "Thank you for registering with SmartBursary. To complete your registration, please verify your email address using the code below:"
        expiry_note = "If you didn't request this code, please ignore this email."
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">{title}</h2>
            <p>Dear {full_name},</p>
            <p>{message}</p>
            <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center;">
                <h1 style="color: #2563eb; font-size: 36px; letter-spacing: 8px; margin: 0;">{otp_code}</h1>
            </div>
            <p>This code will expire in <strong>10 minutes</strong>.</p>
            <p>{expiry_note}</p>
            <p style="margin-top: 30px;">Best regards,<br>SmartBursary Team</p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
{title}

Dear {full_name},

{message}

{otp_code}

This code will expire in 10 minutes.

{expiry_note}

Best regards,
SmartBursary Team
    """
    
    send_email(email, subject, html_body, text_body)


def send_staff_account_otp(email: str, full_name: str, otp_code: str, role: str):
    """Send OTP email for newly created staff account."""
    subject = f"Verify Your SmartBursary {role.title()} Account"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .otp-box {{ background: white; border: 2px solid #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
            .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>SmartBursary Account Created</h1>
            </div>
            <div class="content">
                <h2>Hello {full_name},</h2>
                <p>A <strong>{role.title()}</strong> account has been created for you on SmartBursary.</p>
                
                <p>To activate your account and set your password, please verify your email address using the code below:</p>
                
                <div class="otp-box">
                    <p style="margin: 0 0 10px 0; font-size: 14px; color: #666;">Your Verification Code</p>
                    <div class="otp-code">{otp_code}</div>
                    <p style="margin: 10px 0 0 0; font-size: 12px; color: #999;">This code expires in 10 minutes</p>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong> This code was requested by a system administrator. If you did not expect this email, please contact your administrator immediately.
                </div>
                
                <p><strong>Next Steps:</strong></p>
                <ol>
                    <li>Click the activation link in your welcome email</li>
                    <li>Enter this 6-digit code</li>
                    <li>Set your secure password</li>
                    <li>Start using SmartBursary</li>
                </ol>
                
                <div class="footer">
                    <p>SmartBursary - Education Financial Assistance</p>
                    <p>This is an automated message, please do not reply.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    SmartBursary Account Created
    
    Hello {full_name},
    
    A {role.title()} account has been created for you on SmartBursary.
    
    Your Verification Code: {otp_code}
    (This code expires in 10 minutes)
    
    Security Notice: This code was requested by a system administrator. 
    If you did not expect this email, please contact your administrator immediately.
    
    Next Steps:
    1. Click the activation link in your welcome email
    2. Enter this 6-digit code
    3. Set your secure password
    4. Start using SmartBursary
    
    SmartBursary - Education Financial Assistance
    """
    
    return send_email(email, subject, html_body, text_body)
