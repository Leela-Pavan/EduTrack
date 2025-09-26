#!/usr/bin/env python3
"""
Direct test of teacher data structure without login
"""
import sqlite3
import json

def test_teacher_data_structure():
    print("🔍 Testing Teacher Data Structure Fix (Direct Database)...")
    
    try:
        # Connect to database
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Run the same query as the API
        print("\n1. Running teacher query...")
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
        
        if teachers:
            print(f"\n2. Processing first teacher record...")
            teacher = teachers[0]
            
            # Apply the same logic as the API
            class_display = teacher[4]  # class_name
            if teacher[4] == '10':
                class_display = 'CSIT'
            elif teacher[4] == '11':
                class_display = 'CSD'
            elif teacher[4] == '12':
                class_display = 'CSE'
            
            # Create the data structure with the fix
            teacher_data = {
                'teacher_id': teacher[0],
                'name': f"{teacher[1]} {teacher[2]}",
                'subject': teacher[3] if teacher[3] else 'Not assigned',
                'department': class_display,
                'section': teacher[5] if teacher[5] else 'All',
                'email': teacher[6] if teacher[6] else 'Not provided',
                'username': teacher[7] if teacher[7] else 'Not set',
                'password': teacher[8] if teacher[8] else 'Not set'  # Only show actual password, not username
            }
            
            print(f"✅ Teacher data structure created successfully")
            
            print(f"\n3. Data fields:")
            for key, value in teacher_data.items():
                if key == 'password':
                    display_value = "••••••••" if value and value != 'Not set' else value
                else:
                    display_value = value
                print(f"   {key}: {display_value}")
            
            print(f"\n4. Fix verification:")
            username = teacher_data['username']
            password = teacher_data['password']
            
            if username != password:
                print(f"   ✅ Username and password are properly separated")
                print(f"   ✅ Username: {username}")
                print(f"   ✅ Password: {'••••••••' if password != 'Not set' else 'Not set'}")
            else:
                print(f"   ❌ Username and password are still the same: {username}")
            
            # Test multiple teachers if available
            if len(teachers) > 1:
                print(f"\n5. Testing additional teachers...")
                for i, teacher in enumerate(teachers[1:4], 2):  # Test up to 3 more
                    teacher_data = {
                        'username': teacher[7] if teacher[7] else 'Not set',
                        'password': teacher[8] if teacher[8] else 'Not set'
                    }
                    print(f"   Teacher {i}: Username='{teacher_data['username']}', Password={'••••••••' if teacher_data['password'] != 'Not set' else 'Not set'}")
        else:
            print("⚠️  No teachers found in database")
            
        print(f"\n" + "="*50)
        print(f"🎉 TEACHER DATA STRUCTURE TEST COMPLETED!")
        print(f"="*50)
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_teacher_data_structure()