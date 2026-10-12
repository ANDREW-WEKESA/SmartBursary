"""Enable and verify email for andrewwekesa675@gmail.com"""
import os
os.environ["DATABASE_URL"] = "postgresql://smartbursary:9EDdU99BRmRRxMTNr5bG028f9qW5yzCP@dpg-db4a5t142hec73al15kg-a/smartbursary"

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://smartbursary:9EDdU99BRmRRxMTNr5bG028f9qW5yzCP@dpg-db4a5t142hec73al15kg-a/smartbursary"

def enable_email():
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as db:
        # Update the user
        result = db.execute(
            text("""
                UPDATE "user" 
                SET email_verified = true, active = true
                WHERE email = 'andrewwekesa675@gmail.com'
                RETURNING id, full_name, email, role, email_verified, active
            """)
        )
        
        user = result.fetchone()
        
        if user:
            db.commit()
            print("✅ User enabled successfully!")
            print(f"   ID: {user[0]}")
            print(f"   Name: {user[1]}")
            print(f"   Email: {user[2]}")
            print(f"   Role: {user[3]}")
            print(f"   Email Verified: {user[4]}")
            print(f"   Active: {user[5]}")
        else:
            print("❌ User not found!")
            
            # Try to find the user
            result = db.execute(
                text("""
                    SELECT id, full_name, email, role, email_verified, active
                    FROM "user" 
                    WHERE email LIKE '%andrewwekesa%'
                """)
            )
            
            users = result.fetchall()
            if users:
                print("\nFound similar users:")
                for u in users:
                    print(f"   - {u[2]} (ID: {u[0]}, Role: {u[3]}, Verified: {u[4]}, Active: {u[5]})")

if __name__ == "__main__":
    enable_email()
