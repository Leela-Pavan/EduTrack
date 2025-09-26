#!/usr/bin/env python3
"""
Add sample passwords for teachers to test password display
"""
import sqlite3
import hashlib

def add_sample_passwords():
    print("🔐 Adding Sample Passwords for Teachers...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check current password storage
        cursor.execute("SELECT user_id, plain_password FROM admin_password_store")
        existing_passwords = cursor.fetchall()
        print(f"Existing passwords: {len(existing_passwords)}")
        
        # Get teacher user IDs
        cursor.execute('''
            SELECT u.id, u.username, t.teacher_id 
            FROM users u 
            JOIN teachers t ON u.id = t.user_id 
            WHERE u.role = 'teacher'
            LIMIT 3
        ''')
        
        teachers = cursor.fetchall()
        print(f"Found {len(teachers)} teacher users")
        
        # Add sample passwords for first 3 teachers
        sample_passwords = ['teach123', 'pass456', 'secure789']
        
        for i, (user_id, username, teacher_id) in enumerate(teachers):
            if i < len(sample_passwords):
                password = sample_passwords[i]
                
                # Hash password for users table
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                # Update users table with hashed password
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
                
                # Insert/update plain password in admin_password_store
                cursor.execute('''
                    INSERT OR REPLACE INTO admin_password_store (user_id, plain_password) 
                    VALUES (?, ?)
                ''', (user_id, password))
                
                print(f"✅ Set password for {username} (Teacher ID: {teacher_id}): {password}")
        
        conn.commit()
        conn.close()
        
        print(f"\n🎉 Sample passwords added successfully!")
        print(f"Now test the teacher details display to see passwords.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_sample_passwords()