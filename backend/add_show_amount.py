"""
Migration script to add show_amount column to bursaries table
Run this once: python add_show_amount.py
"""
import sqlite3

db_path = "smartbursary.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column already exists
    cursor.execute("PRAGMA table_info(bursaries)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "show_amount" not in columns:
        print("Adding show_amount column to bursaries table...")
        cursor.execute("ALTER TABLE bursaries ADD COLUMN show_amount INTEGER DEFAULT 1")
        conn.commit()
        print("✓ show_amount column added successfully")
    else:
        print("✓ show_amount column already exists")
        
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("Migration complete!")
