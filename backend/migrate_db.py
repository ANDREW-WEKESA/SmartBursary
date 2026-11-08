"""
Add missing ward column to users table
Run this with: python migrate_db.py
"""
import sqlite3

db_path = "smartbursary.db"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Add missing columns
    if 'ward' not in columns:
        print("Adding 'ward' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN ward TEXT DEFAULT ''")
        conn.commit()
        print("✅ Added 'ward' column!")
    else:
        print("✅ 'ward' column already exists")
    
    if 'last_login' not in columns:
        print("Adding 'last_login' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
        conn.commit()
        print("✅ Added 'last_login' column!")
    else:
        print("✅ 'last_login' column already exists")
    
    if 'login_count' not in columns:
        print("Adding 'login_count' column...")
        cursor.execute("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0")
        conn.commit()
        print("✅ Added 'login_count' column!")
    else:
        print("✅ 'login_count' column already exists")
    
    conn.close()
    print("\n✅ Database migration complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

