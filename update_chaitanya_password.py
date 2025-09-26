#!/usr/bin/env python3
"""
Update Chaitanya Reddy's password to 2580
"""
import sqlite3

def update_chaitanya_password():
    print("🔐 Updating Chaitanya Reddy's Password...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Find Chaitanya Reddy's user ID
        cursor.execute('''
            SELECT u.id, u.username, t.first_name, t.last_name
            FROM users u 
            JOIN teachers t ON u.id = t.user_id 
            WHERE u.role = 'teacher' 
            AND (t.first_name LIKE '%Chaitanya%' OR u.username LIKE '%Chaithu%')
        ''')
        
        chaitanya = cursor.fetchone()
        
        if chaitanya:
            user_id, username, first_name, last_name = chaitanya
            full_name = f"{first_name or ''} {last_name or ''}".strip()
            
            print(f"Found: {full_name} (Username: {username})")
            
            # Update password in admin_password_store
            cursor.execute('''
                UPDATE admin_password_store 
                SET plain_password = ? 
                WHERE user_id = ?
            ''', ("2580", user_id))
            
            if cursor.rowcount > 0:
                print(f"✅ Password updated successfully!")
                print(f"   User: {full_name} ({username})")
                print(f"   New Password: 2580")
            else:
                print(f"❌ No password entry found to update")
            
            conn.commit()
            
            # Verify the change
            cursor.execute('''
                SELECT plain_password 
                FROM admin_password_store 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if result:
                print(f"✅ Verification: Password is now '{result[0]}'")
            
        else:
            print("❌ Chaitanya Reddy not found in database")
        
        conn.close()
        
        print(f"\n🎉 Password update completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_chaitanya_password()