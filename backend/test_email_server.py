#!/usr/bin/env python3
"""
Simple SMTP test server for testing email notifications locally.
This creates a fake SMTP server that prints emails to the console.

Run this in a separate terminal:
    python test_email_server.py

Then run your backend with EMAIL_ENABLED=true and SMTP_PORT=1025

Note: Requires aiosmtpd library. Install with:
    pip install aiosmtpd
"""

import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP as SMTPProtocol
from datetime import datetime

class TestSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print("\n" + "="*80)
        print(f"📧 EMAIL RECEIVED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"From: {envelope.mail_from}")
        print(f"To: {', '.join(envelope.rcpt_tos)}")
        print(f"Peer: {session.peer}")
        print("-"*80)
        print("Content:")
        print(envelope.content.decode('utf-8', errors='replace'))
        print("="*80 + "\n")
        return '250 Message accepted for delivery'

async def main():
    print("🚀 Starting test SMTP server on localhost:1025")
    print("📬 All emails will be printed to this console")
    print("Press Ctrl+C to stop\n")
    
    handler = TestSMTPHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=1025)
    controller.start()
    
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour at a time
    except KeyboardInterrupt:
        print("\n👋 Shutting down SMTP test server")
    finally:
        controller.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
