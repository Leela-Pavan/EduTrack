import sqlite3
from werkzeug.security import check_password_hash

def debug_student_login():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()

    # Test 1: Check if student exists
    print("=== Testing Student Login Debug ===")
    cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', ('student1',))
    user = cursor.fetchone()
    
    if user:
        print(f"✓ User found: ID={user[0]}, Username={user[1]}, Role={user[3]}")
        
        # Test password
        if check_password_hash(user[2], 'password123'):
            print("✓ Password verification successful")
            
            # Test student profile lookup
            cursor.execute('''SELECT s.*, u.username FROM students s 
                             JOIN users u ON s.user_id = u.id WHERE u.id = ?''', (user[0],))
            student = cursor.fetchone()
            
            if student:
                print(f"✓ Student profile found: {student[2]} {student[3]}, Class: {student[4]}{student[5]}")
                
                # Test attendance query
                cursor.execute('''SELECT COUNT(*) as total, 
                                 SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                                 SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                                 FROM attendance WHERE student_id = ? AND date >= date('now', '-30 days')''', 
                               (student[0],))
                attendance_summary = cursor.fetchone()
                print(f"✓ Attendance summary: Total={attendance_summary[0]}, Present={attendance_summary[1]}, Absent={attendance_summary[2]}")
                
                # Test timetable query
                from datetime import datetime
                today = datetime.now().strftime('%A')
                cursor.execute('''SELECT * FROM timetable WHERE class_name = ? AND section = ? AND day_of_week = ? 
                                 ORDER BY period_number''', (student[4], student[5], today))
                timetable = cursor.fetchall()
                print(f"✓ Timetable for {today}: {len(timetable)} periods found")
                
                # Test suggested tasks query
                cursor.execute('''SELECT * FROM suggested_tasks WHERE student_id = ? 
                                 ORDER BY priority DESC, created_at DESC''', (student[0],))
                suggested_tasks = cursor.fetchall()
                print(f"✓ Suggested tasks: {len(suggested_tasks)} tasks found")
                
                print("=== All database queries successful! ===")
                
            else:
                print("✗ Student profile not found")
        else:
            print("✗ Password verification failed")
    else:
        print("✗ User not found")
    
    conn.close()

if __name__ == '__main__':
    debug_student_login()