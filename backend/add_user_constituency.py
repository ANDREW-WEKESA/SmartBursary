"""Add constituency column to users table"""
import sqlite3

db_path = "smartbursary.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Add constituency column to users
    cursor.execute("ALTER TABLE users ADD COLUMN constituency TEXT DEFAULT ''")
    conn.commit()
    print("✓ Added constituency column to users table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("✓ constituency column already exists in users table")
    else:
        raise

conn.close()
print("Migration complete!")
