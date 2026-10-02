"""
Database migration script to add profile fields to existing database.
Run this to update an existing database without losing data.
"""
import sqlite3
import os

DB_PATH = "smartbursary.db"

# Check if database exists
if not os.path.exists(DB_PATH):
    print(f"Database {DB_PATH} not found. Run the backend first to create it.")
    exit(1)

# Add missing columns to users table
ADD_COLUMNS = """
ALTER TABLE users ADD COLUMN profile_complete INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN date_of_birth DATE;
ALTER TABLE users ADD COLUMN national_id VARCHAR(100) DEFAULT '';
ALTER TABLE users ADD COLUMN gender VARCHAR(20) DEFAULT '';
ALTER TABLE users ADD COLUMN county VARCHAR(100) DEFAULT '';
ALTER TABLE users ADD COLUMN sub_county VARCHAR(100) DEFAULT '';
ALTER TABLE users ADD COLUMN address TEXT DEFAULT '';
ALTER TABLE users ADD COLUMN guardian_name VARCHAR(160) DEFAULT '';
ALTER TABLE users ADD COLUMN guardian_phone VARCHAR(40) DEFAULT '';
ALTER TABLE users ADD COLUMN guardian_relationship VARCHAR(50) DEFAULT '';
ALTER TABLE users ADD COLUMN institution VARCHAR(180) DEFAULT '';
ALTER TABLE users ADD COLUMN student_number VARCHAR(100) DEFAULT '';
ALTER TABLE users ADD COLUMN course VARCHAR(180) DEFAULT '';
ALTER TABLE users ADD COLUMN year_of_study VARCHAR(40) DEFAULT '';
ALTER TABLE users ADD COLUMN admission_year INTEGER;
ALTER TABLE users ADD COLUMN monthly_household_income INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN household_size INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN has_national_id_doc INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN has_student_id_doc INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN has_admission_letter INTEGER DEFAULT 0;
"""

# Create profile_documents table
CREATE_PROFILE_DOCUMENTS = """
CREATE TABLE IF NOT EXISTS profile_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_type VARCHAR(180) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL UNIQUE,
    content_type VARCHAR(120) DEFAULT 'application/octet-stream',
    size_bytes INTEGER DEFAULT 0,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Add columns one by one (ignore errors if they already exist)
    columns = [
        ("profile_complete", "INTEGER DEFAULT 0"),
        ("date_of_birth", "DATE"),
        ("national_id", "VARCHAR(100) DEFAULT ''"),
        ("gender", "VARCHAR(20) DEFAULT ''"),
        ("county", "VARCHAR(100) DEFAULT ''"),
        ("sub_county", "VARCHAR(100) DEFAULT ''"),
        ("address", "TEXT DEFAULT ''"),
        ("guardian_name", "VARCHAR(160) DEFAULT ''"),
        ("guardian_phone", "VARCHAR(40) DEFAULT ''"),
        ("guardian_relationship", "VARCHAR(50) DEFAULT ''"),
        ("institution", "VARCHAR(180) DEFAULT ''"),
        ("student_number", "VARCHAR(100) DEFAULT ''"),
        ("course", "VARCHAR(180) DEFAULT ''"),
        ("year_of_study", "VARCHAR(40) DEFAULT ''"),
        ("admission_year", "INTEGER"),
        ("monthly_household_income", "INTEGER DEFAULT 0"),
        ("household_size", "INTEGER DEFAULT 1"),
        ("has_national_id_doc", "INTEGER DEFAULT 0"),
        ("has_student_id_doc", "INTEGER DEFAULT 0"),
        ("has_admission_letter", "INTEGER DEFAULT 0"),
    ]
    
    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"✓ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"✓ Column already exists: {col_name}")
            else:
                print(f"✗ Error adding {col_name}: {e}")
    
    # Create profile_documents table
    try:
        cursor.execute(CREATE_PROFILE_DOCUMENTS)
        print("✓ Created profile_documents table")
    except sqlite3.OperationalError as e:
        if "already exists" in str(e):
            print("✓ profile_documents table already exists")
        else:
            print(f"✗ Error creating profile_documents table: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database migration completed successfully!")
    print("The database now has all the required profile fields.")
    
except Exception as e:
    print(f"✗ Migration failed: {e}")
    exit(1)