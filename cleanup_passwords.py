#!/usr/bin/env python3
"""
Clean up duplicate password entries and ensure proper password assignments
"""
import sqlite3

def cleanup_passwords():
    print("🧹 Cleaning Up Password Storage...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # First, remove all existing entries from admin_password_store
        print("1. Removing duplicate entries...")
        cursor.execute("DELETE FROM admin_password_store")
        
        # Get all teachers
        cursor.execute('''
            SELECT u.id, u.username, t.first_name, t.last_name, t.teacher_id
            FROM users u 
            JOIN teachers t ON u.id = t.user_id 
            WHERE u.role = 'teacher'
        ''')
        
        teachers = cursor.fetchall()
        print(f"2. Found {len(teachers)} teachers")
        
        # Set passwords properly
        for user_id, username, first_name, last_name, teacher_id in teachers:
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            
            # Check if this is Chaitanya Reddy - keep his existing password
            if 'Chaitanya' in full_name and 'Reddy' in full_name:
                password = "teach123"  # Keep his original password
                print(f"   Keeping Chaitanya Reddy's password: {password}")
            else:
                password = "1234"  # Set to 1234 for all others
                print(f"   Setting {username} ({full_name or username}) password: {password}")
            
            # Insert clean password entry
            cursor.execute('''
                INSERT INTO admin_password_store (user_id, plain_password) 
                VALUES (?, ?)
            ''', (user_id, password))
        
        conn.commit()
        
        # Final verification
        print(f"\n3. ✅ Final verification - Clean password list:")
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
        
        print(f"\n🎉 Password cleanup completed!")
        print(f"📋 Summary:")
        print(f"   - Chaitanya Reddy: teach123 (unchanged)")
        print(f"   - All other teachers: 1234")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    cleanup_passwords()