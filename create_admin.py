#!/usr/bin/env python3
"""
Script to create/recreate the admin account in EduTrack database.
Run this script to ensure the admin account exists.
"""

import sqlite3
from werkzeug.security import generate_password_hash

def create_admin_account():
    """Create the admin account in the database."""
    print("Creating admin account...")
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Delete existing admin account if any
    cursor.execute('DELETE FROM users WHERE username = ?', ('ADMIN',))
    
    # Create admin account
    admin_password_hash = generate_password_hash('ADMIN')
    cursor.execute('''INSERT INTO users (username, password_hash, role, email, mobile_number) 
                     VALUES (?, ?, ?, ?, ?)''',
                 ('ADMIN', admin_password_hash, 'admin', 'admin@edutrack.com', ''))
    
    conn.commit()
    conn.close()
    
    print("✅ Admin account created successfully!")
    print("Username: ADMIN")
    print("Password: ADMIN")
    print("Email: admin@edutrack.com")

if __name__ == "__main__":
    create_admin_account()