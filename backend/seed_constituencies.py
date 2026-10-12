"""
Seed all 290 constituencies as bursary programs
Run this script once to populate the database with all Kenya constituencies
"""
from app.database import SessionLocal
from app.models import Bursary
from app.kenya_counties_constituencies import KENYA_COUNTIES_CONSTITUENCIES
from datetime import date
import json

def seed_all_constituencies():
    """Create bursary programs for all 290 constituencies"""
    db = SessionLocal()
    
    try:
        print("🇰🇪 Seeding all Kenya constituencies...")
        print(f"Total: {sum(len(c) for c in KENYA_COUNTIES_CONSTITUENCIES.values())} constituencies")
        print(f"Counties: {len(KENYA_COUNTIES_CONSTITUENCIES)}\n")
        
        count = 0
        skipped = 0
        
        for county, constituencies in sorted(KENYA_COUNTIES_CONSTITUENCIES.items()):
            print(f"\n📍 {county} County ({len(constituencies)} constituencies)")
            
            for constituency in sorted(constituencies):
                # Check if already exists
                existing = db.query(Bursary).filter(
                    Bursary.name == f"{constituency} CDF Bursary",
                    Bursary.constituency == constituency
                ).first()
                
                if existing:
                    print(f"   ⏭️  {constituency} - already exists")
                    skipped += 1
                    continue
                
                # Create bursary program
                bursary = Bursary(
                    name=f"{constituency} CDF Bursary",
                    description=f"Constituency Development Fund bursary for eligible students from {constituency} constituency, {county} County.",
                    eligibility=f"Must be a resident of {constituency} constituency and enrolled in a recognized educational institution (secondary, TVET, college or university).",
                    constituency=constituency,
                    amount_kes=20000,  # Standard amount
                    show_amount=True,
                    deadline=date(2027, 3, 31),  # Default deadline
                    required_documents=json.dumps([
                        "National ID or Birth Certificate",
                        "Admission Letter or Student ID",
                        "Fee Structure",
                        "Parent/Guardian ID Copy"
                    ]),
                    active=True
                )
                
                db.add(bursary)
                count += 1
                print(f"   ✅ {constituency}")
        
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS!")
        print(f"{'='*60}")
        print(f"Created: {count} new bursaries")
        print(f"Skipped: {skipped} existing bursaries")
        print(f"Total in database: {db.query(Bursary).count()}")
        print(f"\n🎉 All 290 constituencies are now in the system!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERROR: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_all_constituencies()
