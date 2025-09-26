#!/usr/bin/env python3
"""
Set all teacher passwords to 1234 except Chaitanya Reddy
"""
import sqlite3

def set_teacher_passwords():
    print("🔐 Setting Teacher Passwords...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Get all teachers with their user info
        cursor.execute('''
            SELECT u.id, u.username, t.first_name, t.last_name, t.teacher_id
            FROM users u 
            JOIN teachers t ON u.id = t.user_id 
            WHERE u.role = 'teacher'
        ''')
        
        teachers = cursor.fetchall()
        print(f"Found {len(teachers)} teachers")
        
        for user_id, username, first_name, last_name, teacher_id in teachers:
            # Check if this is Chaitanya Reddy
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            
            if 'Chaitanya' in full_name and 'Reddy' in full_name:
                print(f"   Skipping Chaitanya Reddy (Username: {username}) - keeping existing password")
                continue
            
            # Set password to 1234 for all other teachers
            password = "1234"
            
            # Insert/update in admin_password_store
            cursor.execute('''
                INSERT OR REPLACE INTO admin_password_store (user_id, plain_password) 
                VALUES (?, ?)
            ''', (user_id, password))
            
            print(f"   ✅ Set password for {username} ({full_name or username}): {password}")
        
        conn.commit()
        
        # Verify the changes
        print(f"\n✅ Verification - All teacher passwords:")
        cursor.execute('''
            SELECT u.username, t.first_name, t.last_name, aps.plain_password 
            FROM admin_password_store aps
            JOIN users u ON aps.user_id = u.id
            JOIN teachers t ON u.id = t.user_id
            ORDER BY u.username
        ''')
        
        stored_passwords = cursor.fetchall()
        
        for username, first_name, last_name, password in stored_passwords:
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            display_name = full_name if full_name else username
            print(f"   {display_name} ({username}): {password}")
        
        conn.close()
        
        print(f"\n🎉 Password update completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    set_teacher_passwords()