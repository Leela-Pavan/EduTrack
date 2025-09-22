"""
Database migration script to add verification fields
Run this script to update the existing database with verification features
"""
import sqlite3
from datetime import datetime

def migrate_database():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    try:
        # Add mobile number and verification fields to users table
        cursor.execute('''
            ALTER TABLE users ADD COLUMN mobile_number TEXT
        ''')
        print("✓ Added mobile_number column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ mobile_number column already exists")
        else:
            print(f"✗ Error adding mobile_number: {e}")
    
    try:
        cursor.execute('''
            ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
        ''')
        print("✓ Added email_verified column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ email_verified column already exists")
        else:
            print(f"✗ Error adding email_verified: {e}")
    
    try:
        cursor.execute('''
            ALTER TABLE users ADD COLUMN mobile_verified BOOLEAN DEFAULT FALSE
        ''')
        print("✓ Added mobile_verified column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ mobile_verified column already exists")
        else:
            print(f"✗ Error adding mobile_verified: {e}")
    
    # Create verification_codes table
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                email TEXT,
                mobile_number TEXT,
                email_code TEXT,
                mobile_code TEXT,
                email_code_expiry TIMESTAMP,
                mobile_code_expiry TIMESTAMP,
                email_attempts INTEGER DEFAULT 0,
                mobile_attempts INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        print("✓ Created verification_codes table")
    except sqlite3.OperationalError as e:
        print(f"✗ Error creating verification_codes table: {e}")
    
    # Add mobile_number to students table
    try:
        cursor.execute('''
            ALTER TABLE students ADD COLUMN mobile_number TEXT
        ''')
        print("✓ Added mobile_number column to students table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ mobile_number column already exists in students table")
        else:
            print(f"✗ Error adding mobile_number to students: {e}")
    
    conn.commit()
    conn.close()
    print("Database migration completed!")

if __name__ == "__main__":
    migrate_database()