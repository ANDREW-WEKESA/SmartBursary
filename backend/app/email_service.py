import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging
import random
from .config import settings

logger = logging.getLogger(__name__)


def generate_otp() -> str:
    """Generate a 6-digit OTP code."""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_email(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Send an email using configured SMTP settings."""
    if not settings.email_enabled:
        logger.info(f"Email disabled. Would have sent to {to_email}: {subject}")
        return False
    
    try:
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
        
        # Connect to SMTP server
        if settings.smtp_port == 465:
            # SSL
            with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_username:
                    server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
        else:
            # TLS or plain
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_port == 587:
                    server.starttls()
                if settings.smtp_username:
                    server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
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


def send_otp_email(email: str, full_name: str, otp_code: str):
    """Send OTP verification email for registration."""
    subject = "Verify Your Email - SmartBursary"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Email Verification</h2>
            <p>Dear {full_name},</p>
            <p>Thank you for registering with SmartBursary. To complete your registration, please verify your email address using the code below:</p>
            <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center;">
                <h1 style="color: #2563eb; font-size: 36px; letter-spacing: 8px; margin: 0;">{otp_code}</h1>
            </div>
            <p>This code will expire in <strong>10 minutes</strong>.</p>
            <p>If you didn't request this code, please ignore this email.</p>
            <p style="margin-top: 30px;">Best regards,<br>SmartBursary Team</p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
Email Verification

Dear {full_name},

Thank you for registering with SmartBursary. To complete your registration, please verify your email address using the code below:

{otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
SmartBursary Team
    """
    
    send_email(email, subject, html_body, text_body)
