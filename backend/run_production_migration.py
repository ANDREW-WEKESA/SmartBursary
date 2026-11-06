"""
Production-safe migration script for SmartBursary database
Adds missing columns: ward, last_login, login_count
Compatible with both SQLite and PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect, Column, Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError

def detect_database_type(connection_string: str) -> str:
    """Detect if database is PostgreSQL or SQLite"""
    if connection_string.startswith('postgresql'):
        return 'postgresql'
    elif connection_string.startswith('sqlite'):
        return 'sqlite'
    else:
        return 'unknown'

def column_exists(inspector, table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table"""
    try:
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns
    except Exception as e:
        print(f"Warning: Could not inspect {table_name}: {e}")
        return False

def add_column_safe(connection, table_name: str, column_name: str, column_type: str, db_type: str):
    """Add a column only if it doesn't exist"""
    inspector = inspect(connection)
    
    if column_exists(inspector, table_name, column_name):
        print(f"✓ Column {table_name}.{column_name} already exists - skipping")
        return True
    
    try:
        # Build ALTER TABLE statement based on database type
        if db_type == 'postgresql':
            sql = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        else:  # SQLite
            sql = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        
        connection.execute(sql)
        connection.commit()
        print(f"✓ Successfully added column {table_name}.{column_name}")
        return True
    except SQLAlchemyError as e:
        connection.rollback()
        print(f"✗ Failed to add column {table_name}.{column_name}: {e}")
        return False

def run_migration():
    """Run the production migration"""
    print("=" * 60)
    print("SmartBursary Production Migration")
    print("=" * 60)
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./smartbursary.db')
    print(f"\nDatabase: {database_url}")
    
    # Detect database type
    db_type = detect_database_type(database_url)
    print(f"Database type: {db_type.upper()}")
    
    if db_type == 'unknown':
        print("\n✗ Unsupported database type")
        return False
    
    try:
        # Create engine and connection
        engine = create_engine(database_url)
        connection = engine.connect()
        print("✓ Connected to database")
        
        # Define migrations
        migrations = []
        
        # Column definitions based on database type
        if db_type == 'postgresql':
            migrations = [
                ('users', 'ward', 'VARCHAR(100) DEFAULT \'\''),
                ('users', 'last_login', 'TIMESTAMP NULL'),
                ('users', 'login_count', 'INTEGER DEFAULT 0'),
            ]
        else:  # SQLite
            migrations = [
                ('users', 'ward', 'TEXT DEFAULT \'\''),
                ('users', 'last_login', 'DATETIME'),
                ('users', 'login_count', 'INTEGER DEFAULT 0'),
            ]
        
        print(f"\nRunning {len(migrations)} migration(s)...")
        print("-" * 60)
        
        success_count = 0
        for table, column, col_type in migrations:
            if add_column_safe(connection, table, column, col_type, db_type):
                success_count += 1
        
        connection.close()
        
        print("-" * 60)
        print(f"\nMigration complete: {success_count}/{len(migrations)} successful")
        
        if success_count == len(migrations):
            print("✓ All migrations applied successfully")
            return True
        else:
            print("⚠ Some migrations failed - check logs above")
            return False
            
    except SQLAlchemyError as e:
        print(f"\n✗ Database connection error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables from .env file if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ Loaded .env file")
    except ImportError:
        print("⚠ python-dotenv not installed - using system environment only")
    
    success = run_migration()
    sys.exit(0 if success else 1)
