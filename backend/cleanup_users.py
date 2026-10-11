"""
Clean up database - keep only 5 essential accounts
Run this with: python cleanup_users.py
"""
from app.database import SessionLocal
from app.models import User, Application, Document, Bursary
from sqlalchemy import select

def cleanup_database():
    db = SessionLocal()
    
    try:
        print("🧹 Cleaning up database...")
        
        # Keep these 5 accounts
        keep_emails = [
            'admin@smartbursary.com',           # Super admin
            'admin.westlands@smartbursary.com', # Constituency admin
            'reviewer.westlands@smartbursary.com', # Reviewer
            'john.wanjiku0@student.ke',         # Applicant 1
            'mary.kamau1@student.ke'            # Applicant 2
        ]
        
        # Get all users
        all_users = db.scalars(select(User)).all()
        print(f"\n📊 Found {len(all_users)} total users")
        
        # Separate users to keep and delete
        users_to_keep = []
        users_to_delete = []
        
        for user in all_users:
            if user.email in keep_emails:
                users_to_keep.append(user)
            else:
                users_to_delete.append(user)
        
        print(f"✅ Keeping {len(users_to_keep)} users:")
        for user in users_to_keep:
            print(f"   - {user.email} ({user.role})")
        
        print(f"\n🗑️  Deleting {len(users_to_delete)} users...")
        
        # Delete applications and documents for users being deleted
        for user in users_to_delete:
            # Delete documents for this user's applications
            applications = db.scalars(select(Application).where(Application.applicant_id == user.id)).all()
            for app in applications:
                # Delete documents
                documents = db.scalars(select(Document).where(Document.application_id == app.id)).all()
                for doc in documents:
                    db.delete(doc)
                # Delete application
                db.delete(app)
            
            # Delete the user
            db.delete(user)
        
        # Delete excess bursaries - keep only 5 (one per remaining user's constituency)
        all_bursaries = db.scalars(select(Bursary)).all()
        print(f"\n📋 Found {len(all_bursaries)} bursaries")
        
        # Keep only Westlands bursaries (since our test users are there)
        bursaries_to_keep = []
        bursaries_to_delete = []
        
        for bursary in all_bursaries:
            if bursary.constituency == 'Westlands' and len(bursaries_to_keep) < 2:
                bursaries_to_keep.append(bursary)
            elif not bursary.constituency and len(bursaries_to_keep) < 5:
                # Keep some general bursaries
                bursaries_to_keep.append(bursary)
            else:
                bursaries_to_delete.append(bursary)
        
        print(f"✅ Keeping {len(bursaries_to_keep)} bursaries")
        print(f"🗑️  Deleting {len(bursaries_to_delete)} bursaries...")
        
        for bursary in bursaries_to_delete:
            # Delete applications for this bursary
            applications = db.scalars(select(Application).where(Application.bursary_id == bursary.id)).all()
            for app in applications:
                documents = db.scalars(select(Document).where(Document.application_id == app.id)).all()
                for doc in documents:
                    db.delete(doc)
                db.delete(app)
            
            # Delete the bursary
            db.delete(bursary)
        
        # Commit all deletions
        db.commit()
        
        # Final count
        final_user_count = db.scalar(select(User).count())
        final_bursary_count = db.scalar(select(Bursary).count())
        final_app_count = db.scalar(select(Application).count())
        
        print(f"\n✅ Cleanup complete!")
        print(f"📊 Final counts:")
        print(f"   Users: {final_user_count}")
        print(f"   Bursaries: {final_bursary_count}")
        print(f"   Applications: {final_app_count}")
        
        print(f"\n🔑 Remaining accounts:")
        remaining_users = db.scalars(select(User)).all()
        for user in remaining_users:
            password = "ChangeMe123!" if user.email == "admin@smartbursary.com" else (
                "admin123" if user.role == "admin" else (
                "reviewer123" if user.role == "reviewer" else "student123"
            ))
            print(f"   {user.email} / {password} ({user.role})")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_database()
