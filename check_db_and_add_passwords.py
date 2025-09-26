#!/usr/bin/env python3
"""
Check database structure and add sample passwords properly
"""
import sqlite3

def check_database_structure():
    print("🔍 Checking Database Structure...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check users table structure
        print("\n📋 Users table structure:")
        cursor.execute("PRAGMA table_info(users)")
        users_columns = cursor.fetchall()
        for col in users_columns:
            print(f"   {col[1]} ({col[2]})")
        
        # Check admin_password_store table structure
        print("\n📋 admin_password_store table structure:")
        cursor.execute("PRAGMA table_info(admin_password_store)")
        pwd_columns = cursor.fetchall()
        for col in pwd_columns:
            print(f"   {col[1]} ({col[2]})")
        
        # Check sample user data
        print("\n👥 Sample users:")
        cursor.execute("SELECT id, username, email, role FROM users WHERE role = 'teacher' LIMIT 3")
        users = cursor.fetchall()
        for user in users:
            print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
        # Add sample passwords using correct column name
        print("\n🔐 Adding sample passwords...")
        
        sample_passwords = ['teach123', 'pass456', 'secure789']
        
        for i, (user_id, username, email, role) in enumerate(users):
            if i < len(sample_passwords):
                password = sample_passwords[i]
                
                # Insert into admin_password_store
                cursor.execute('''
                    INSERT OR REPLACE INTO admin_password_store (user_id, plain_password) 
                    VALUES (?, ?)
                ''', (user_id, password))
                
                print(f"   ✅ Set password for {username}: {password}")
        
        conn.commit()
        
        # Verify passwords were added
        print(f"\n✅ Verification - Passwords in admin_password_store:")
        cursor.execute('''
            SELECT aps.user_id, u.username, aps.plain_password 
            FROM admin_password_store aps
            JOIN users u ON aps.user_id = u.id
        ''')
        stored_passwords = cursor.fetchall()
        
        for pwd in stored_passwords:
            print(f"   User: {pwd[1]}, Password: {pwd[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database_structure()