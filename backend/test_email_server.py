#!/usr/bin/env python3
"""
Simple SMTP test server for testing email notifications locally.
This creates a fake SMTP server that prints emails to the console.

Run this in a separate terminal:
    python test_email_server.py

Then run your backend with EMAIL_ENABLED=true and SMTP_PORT=1025
"""

import asyncore
from smtpd import SMTPServer
from datetime import datetime

class TestSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print("\n" + "="*80)
        print(f"📧 EMAIL RECEIVED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"From: {mailfrom}")
        print(f"To: {', '.join(rcpttos)}")
        print(f"Peer: {peer}")
        print("-"*80)
        print("Content:")
        print(data.decode('utf-8', errors='replace'))
        print("="*80 + "\n")

if __name__ == "__main__":
    print("🚀 Starting test SMTP server on localhost:1025")
    print("📬 All emails will be printed to this console")
    print("Press Ctrl+C to stop\n")
    
    server = TestSMTPServer(('127.0.0.1', 1025), None)
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("\n👋 Shutting down SMTP test server")
