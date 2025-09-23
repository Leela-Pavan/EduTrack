#!/usr/bin/env python3
"""
Script to check database tables and initialize if needed.
"""

import sqlite3
import os
from app import init_db

def check_database():
    """Check database tables and data."""
    db_path = 'school_system.db'
    
    print(f"Checking database at: {os.path.abspath(db_path)}")
    
    if not os.path.exists(db_path):
        print("❌ Database file does not exist. Creating...")
        init_db()
        print("✅ Database created and initialized.")
    else:
        print("✅ Database file exists.")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n📋 Tables found: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check if admin user exists
    try:
        cursor.execute("SELECT username, role FROM users WHERE role='admin'")
        admin_users = cursor.fetchall()
        print(f"\n👤 Admin users found: {len(admin_users)}")
        for user in admin_users:
            print(f"  - {user[0]} ({user[1]})")
    except Exception as e:
        print(f"❌ Error checking admin users: {e}")
    
    # Check students and teachers count
    try:
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        
        print(f"\n📊 Data summary:")
        print(f"  - Students: {student_count}")
        print(f"  - Teachers: {teacher_count}")
    except Exception as e:
        print(f"❌ Error checking data: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_database()