import sqlite3

def test_direct_insert():
    print("Testing direct database insert...")
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    try:
        # Test 1: Insert into users table
        print("1. Testing users table insert...")
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, 'student', ?)
        ''', ('TEST_USER', 'hash123', 'test@test.com'))
        
        user_id = cursor.lastrowid
        print(f"   ✓ User inserted with ID: {user_id}")
        
        # Test 2: Insert into students table
        print("2. Testing students table insert...")
        cursor.execute('''
            INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'TEST_STUDENT', 'Test', 'Student', 'Computer Science', 'CSIT-A', '1234567890'))
        
        print("   ✓ Student inserted successfully")
        
        # Test 3: Verify data
        print("3. Verifying inserted data...")
        cursor.execute("SELECT * FROM users WHERE username = 'TEST_USER'")
        user_data = cursor.fetchone()
        print(f"   User data: {user_data}")
        
        cursor.execute("SELECT * FROM students WHERE student_id = 'TEST_STUDENT'")
        student_data = cursor.fetchone()
        print(f"   Student data: {student_data}")
        
        # Cleanup
        print("4. Cleaning up...")
        cursor.execute("DELETE FROM students WHERE student_id = 'TEST_STUDENT'")
        cursor.execute("DELETE FROM users WHERE username = 'TEST_USER'")
        
        conn.commit()
        print("✓ All tests passed!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
    
    conn.close()

if __name__ == "__main__":
    test_direct_insert()