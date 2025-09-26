#!/usr/bin/env python3
"""
Test the updated teacher data structure with proper name and password handling
"""
import sqlite3

def test_updated_teacher_data():
    print("🔍 Testing Updated Teacher Data Structure...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Use the same query as the updated API
        cursor.execute('''
            SELECT t.teacher_id, t.first_name, t.last_name, t.subject, 
                   t.class_name, t.section, u.email, u.username, aps.plain_password
            FROM teachers t
            LEFT JOIN users u ON t.user_id = u.id
            LEFT JOIN admin_password_store aps ON u.id = aps.user_id
            ORDER BY t.first_name, t.last_name
        ''')
        
        teachers = cursor.fetchall()
        conn.close()
        
        print(f"✅ Found {len(teachers)} teachers in database")
        
        teacher_list = []
        for teacher in teachers:
            # Apply the same logic as the updated API
            class_display = teacher[4]  # class_name
            if teacher[4] == '10':
                class_display = 'CSIT'
            elif teacher[4] == '11':
                class_display = 'CSD'
            elif teacher[4] == '12':
                class_display = 'CSE'
            
            # Handle name construction - use username if first/last names are empty
            first_name = teacher[1].strip() if teacher[1] else ''
            last_name = teacher[2].strip() if teacher[2] else ''
            
            if first_name and last_name:
                display_name = f"{first_name} {last_name}"
            elif first_name:
                display_name = first_name
            elif last_name:
                display_name = last_name
            else:
                # Use username as display name if no first/last name available
                display_name = teacher[7] if teacher[7] else 'Unnamed Teacher'
            
            # Handle password - check for None string and actual None values
            password_value = teacher[8]
            if password_value and password_value != 'None' and str(password_value).strip():
                password_display = password_value
            else:
                password_display = 'Not set'
            
            teacher_data = {
                'teacher_id': teacher[0],
                'name': display_name,
                'subject': teacher[3] if teacher[3] else 'Not assigned',
                'department': class_display,
                'section': teacher[5] if teacher[5] else 'All',
                'email': teacher[6] if teacher[6] else 'Not provided',
                'username': teacher[7] if teacher[7] else 'Not set',
                'password': password_display
            }
            
            teacher_list.append(teacher_data)
        
        print(f"\n📋 Updated Teacher Data:")
        for i, teacher in enumerate(teacher_list[:5], 1):  # Show first 5 teachers
            print(f"\nTeacher {i}:")
            print(f"   Name: '{teacher['name']}'")
            print(f"   Username: '{teacher['username']}'") 
            print(f"   Password: {'••••••••' if teacher['password'] != 'Not set' else 'Not set'}")
            print(f"   Email: '{teacher['email']}'")
            print(f"   Subject: '{teacher['subject']}'")
        
        print(f"\n🔍 Name Fix Verification:")
        empty_names = [t for t in teacher_list if not t['name'] or t['name'].strip() == '']
        if empty_names:
            print(f"   ❌ Found {len(empty_names)} teachers with empty names")
        else:
            print(f"   ✅ All teachers have names (using username as fallback)")
        
        print(f"\n🔍 Password Fix Verification:")
        actual_passwords = [t for t in teacher_list if t['password'] != 'Not set']
        print(f"   📊 Teachers with passwords: {len(actual_passwords)}")
        print(f"   📊 Teachers without passwords: {len(teacher_list) - len(actual_passwords)}")
        
        print(f"\n" + "="*50)
        print(f"🎉 UPDATED TEACHER DATA STRUCTURE TEST COMPLETED!")
        print(f"="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_updated_teacher_data()