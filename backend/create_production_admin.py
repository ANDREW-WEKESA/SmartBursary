"""
Create admin account directly in production database.
Run this script to create admin@smartbursary.com with password ChangeMe!
"""
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    # Get database URL from environment or use the one you'll provide
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        print("\nUsage:")
        print('set DATABASE_URL=postgresql://user:password@host/database')
        print('python create_production_admin.py')
        return
    
    # PostgreSQL URLs from Render need postgres:// changed to postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"Connecting to database...")
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Hash the password
        hashed_password = pwd_context.hash("ChangeMe!")
        
        # Check if admin already exists
        result = session.execute(
            text("SELECT id, email, active FROM users WHERE email = :email"),
            {"email": "admin@smartbursary.com"}
        )
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"\n⚠️  User admin@smartbursary.com already exists (ID: {existing_user[0]})")
            print(f"   Active: {existing_user[2]}")
            print("\nUpdating password and activating account...")
            
            session.execute(
                text("""
                    UPDATE users 
                    SET password = :password, 
                        active = true, 
                        email_verified = true 
                    WHERE email = :email
                """),
                {"password": hashed_password, "email": "admin@smartbursary.com"}
            )
            session.commit()
            print("✅ Admin account updated successfully!")
            
        else:
            print("\nCreating new admin account...")
            
            session.execute(
                text("""
                    INSERT INTO users (email, password, role, active, email_verified, created_at)
                    VALUES (:email, :password, 'admin', true, true, CURRENT_TIMESTAMP)
                """),
                {"email": "admin@smartbursary.com", "password": hashed_password}
            )
            session.commit()
            print("✅ Admin account created successfully!")
        
        print("\n" + "="*50)
        print("ADMIN CREDENTIALS")
        print("="*50)
        print("Email:    admin@smartbursary.com")
        print("Password: ChangeMe!")
        print("="*50)
        print("\nYou can now login at:")
        print("https://smart-bursary-xijg-git-main-andrew-wekesas-projects.vercel.app/")
        
        session.close()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure:")
        print("1. DATABASE_URL is correct")
        print("2. You have network access to the database")
        print("3. psycopg2-binary is installed: pip install psycopg2-binary")
        sys.exit(1)

if __name__ == "__main__":
    create_admin()
