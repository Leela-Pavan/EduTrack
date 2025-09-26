import sqlite3

def main():
    print("EduTrack Database Debug")
    print("=" * 30)
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check students table
        print("1. Students table schema:")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students';")
        result = cursor.fetchone()
        if result:
            print(result[0])
        else:
            print("Students table not found!")
        
        print("\n2. Teachers table schema:")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='teachers';")
        result = cursor.fetchone()
        if result:
            print(result[0])
        else:
            print("Teachers table not found!")
            
        print("\n3. Current data counts:")
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        print(f"Students: {student_count}")
        
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        print(f"Teachers: {teacher_count}")
        
        print("\n4. Testing insert (will rollback):")
        # Test insert without committing
        cursor.execute("""
            INSERT INTO students (student_id, email, first_name, last_name, department, section, mobile)
            VALUES ('TEST123', 'test@test.com', 'Test', 'User', 'CS', 'CSIT-A', '1234567890')
        """)
        print("Insert test successful - SQL syntax is correct")
        
        # Don't commit - just rollback
        conn.rollback()
        print("Test insert rolled back")
        
        conn.close()
        print("\n✓ Database connection and operations work correctly!")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    main()