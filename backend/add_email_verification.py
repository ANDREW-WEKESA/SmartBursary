#!/usr/bin/env python3
"""
Migration script to add email verification support.
Adds email_verified column to users table and creates email_otps table.
"""

import sqlite3
from pathlib import Path

def migrate():
    db_path = Path(__file__).parent / "smartbursary.db"
    
    if not db_path.exists():
        print(f"❌ Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add email_verified column to users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "email_verified" not in columns:
            print("Adding email_verified column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT 0")
            
            # Set existing users as verified (they registered before this feature)
            cursor.execute("UPDATE users SET email_verified = 1")
            print(f"✅ Marked {cursor.rowcount} existing users as email verified")
        else:
            print("✅ email_verified column already exists")
        
        # Create email_otps table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(254) NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                purpose VARCHAR(50) DEFAULT 'registration',
                expires_at TIMESTAMP NOT NULL,
                verified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ email_otps table created/verified")
        
        # Create index on email for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_otps_email ON email_otps(email)
        """)
        print("✅ Index created on email_otps.email")
        
        conn.commit()
        print("\n🎉 Migration completed successfully!")
        print("\nEmail verification is now enabled:")
        print("- New users must verify their email before logging in")
        print("- OTP codes expire after 10 minutes")
        print("- Existing users are automatically marked as verified")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
