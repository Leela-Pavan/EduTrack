#!/usr/bin/env python3
"""
Debug teacher name and password fields
"""
import sqlite3

def debug_teacher_fields():
    print("🔍 Debugging Teacher Name and Password Fields...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check raw teacher data
        print("\n1. Raw teacher data from database:")
        cursor.execute('''
            SELECT t.teacher_id, t.first_name, t.last_name, t.subject, 
                   t.class_name, t.section, u.email, u.username, aps.plain_password
            FROM teachers t
            LEFT JOIN users u ON t.user_id = u.id
            LEFT JOIN admin_password_store aps ON u.id = aps.user_id
            LIMIT 3
        ''')
        
        teachers = cursor.fetchall()
        
        for i, teacher in enumerate(teachers):
            print(f"\nTeacher {i+1}:")
            print(f"  teacher_id: '{teacher[0]}'")
            print(f"  first_name: '{teacher[1]}'")
            print(f"  last_name: '{teacher[2]}'")
            print(f"  subject: '{teacher[3]}'")
            print(f"  class_name: '{teacher[4]}'")
            print(f"  section: '{teacher[5]}'")
            print(f"  email: '{teacher[6]}'")
            print(f"  username: '{teacher[7]}'")
            print(f"  plain_password: '{teacher[8]}'")
            
            # Test name concatenation
            if teacher[1] and teacher[2]:
                full_name = f"{teacher[1]} {teacher[2]}"
                print(f"  full_name: '{full_name}'")
            elif teacher[1]:
                full_name = teacher[1]
                print(f"  full_name (first only): '{full_name}'")
            elif teacher[2]:
                full_name = teacher[2]
                print(f"  full_name (last only): '{full_name}'")
            else:
                print(f"  full_name: EMPTY (both first_name and last_name are null/empty)")
        
        # Check if names exist in teachers table
        print(f"\n2. Checking teachers table structure:")
        cursor.execute("PRAGMA table_info(teachers)")
        columns = cursor.fetchall()
        
        name_columns = [col for col in columns if 'name' in col[1].lower()]
        print(f"Name-related columns: {[col[1] for col in name_columns]}")
        
        # Check actual data in teachers table
        print(f"\n3. Sample teacher records with all name fields:")
        cursor.execute("SELECT teacher_id, first_name, last_name, name FROM teachers LIMIT 3")
        teachers_with_names = cursor.fetchall()
        
        for teacher in teachers_with_names:
            print(f"  ID: {teacher[0]}, first_name: '{teacher[1]}', last_name: '{teacher[2]}', name: '{teacher[3]}'")
        
        # Check password storage
        print(f"\n4. Checking password storage:")
        cursor.execute("SELECT user_id, plain_password FROM admin_password_store LIMIT 3")
        passwords = cursor.fetchall()
        
        if passwords:
            for pwd in passwords:
                print(f"  User ID: {pwd[0]}, Password: {'••••••••' if pwd[1] else 'NULL'}")
        else:
            print("  No passwords found in admin_password_store")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_teacher_fields()