import sqlite3

def check_registration():
    print("Checking Teacher Registration in Database")
    print("=" * 50)
    
    try:
        # Connect to the database
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check if user exists in users table
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", ('Raju', 'raju@gmail.com'))
        user_record = cursor.fetchone()
        
        if user_record:
            print("✅ User found in users table:")
            print(f"   ID: {user_record[0]}")
            print(f"   Username: {user_record[1]}")
            print(f"   Role: {user_record[3]}")
            print(f"   Email: {user_record[4]}")
            print(f"   Mobile: {user_record[5] if len(user_record) > 5 else 'Not available'}")
            
            # Check if teacher record exists
            cursor.execute("SELECT * FROM teachers WHERE user_id = ?", (user_record[0],))
            teacher_record = cursor.fetchone()
            
            if teacher_record:
                print("\n✅ Teacher record found in teachers table:")
                print(f"   Teacher ID: {teacher_record[2]}")
                print(f"   Name: {teacher_record[3]} {teacher_record[4]}")
                print(f"   Subject: {teacher_record[5]}")
                print(f"   Designation: {teacher_record[6]}")
                print(f"   Mobile: {teacher_record[8] if len(teacher_record) > 8 else 'Not available'}")
                
                print("\n🎉 REGISTRATION SUCCESSFUL!")
                print("Teacher 'Raju' has been successfully registered in the system.")
            else:
                print("\n❌ Teacher record NOT found in teachers table.")
                print("Registration may have failed at teacher profile creation.")
        else:
            print("❌ User NOT found in database.")
            print("Registration has not been completed yet or failed.")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 50)

def list_all_teachers():
    print("\nAll Teachers in Database:")
    print("-" * 30)
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.teacher_id, t.first_name, t.last_name, t.subject, t.class_name, u.email 
            FROM teachers t 
            JOIN users u ON t.user_id = u.id
        """)
        teachers = cursor.fetchall()
        
        if teachers:
            for teacher in teachers:
                print(f"ID: {teacher[0]} | Name: {teacher[1]} {teacher[2]} | Subject: {teacher[3]} | Email: {teacher[5]}")
        else:
            print("No teachers found in database.")
            
        conn.close()
        
    except Exception as e:
        print(f"Error listing teachers: {e}")

if __name__ == "__main__":
    check_registration()
    list_all_teachers()