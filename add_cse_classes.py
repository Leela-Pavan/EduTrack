import sqlite3
from werkzeug.security import generate_password_hash

def add_cse_classes():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Add CSE classes to timetable
    cse_classes = [
        ('CSE', 'A', 'Monday', 1, 'Data Structures', 1, '09:00', '10:00'),
        ('CSE', 'A', 'Tuesday', 2, 'Algorithms', 1, '10:00', '11:00'),
        ('CSE', 'A', 'Wednesday', 3, 'Database Systems', 1, '11:00', '12:00'),
        ('CSE', 'B', 'Monday', 1, 'Computer Networks', 1, '09:00', '10:00'),
        ('CSE', 'B', 'Tuesday', 2, 'Operating Systems', 1, '10:00', '11:00'),
        ('CSE', 'B', 'Wednesday', 3, 'Software Engineering', 1, '11:00', '12:00'),
        ('CSE', 'C', 'Monday', 1, 'Machine Learning', 1, '09:00', '10:00'),
        ('CSE', 'C', 'Tuesday', 2, 'AI Fundamentals', 1, '10:00', '11:00'),
        ('CSE', 'C', 'Wednesday', 3, 'Deep Learning', 1, '11:00', '12:00'),
    ]
    
    for class_info in cse_classes:
        cursor.execute('''
            INSERT OR IGNORE INTO timetable 
            (class_name, section, day_of_week, period_number, subject, teacher_id, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', class_info)
    
    # Add sample students to CSE classes
    cse_students = [
        (1, 'CSE-A-001', 'Arjun', 'Kumar', 'CSE', 'A', '', '', '', '9876543210'),
        (1, 'CSE-A-002', 'Priya', 'Sharma', 'CSE', 'A', '', '', '', '9876543211'),
        (1, 'CSE-A-003', 'Rahul', 'Singh', 'CSE', 'A', '', '', '', '9876543212'),
        (1, 'CSE-B-001', 'Anita', 'Gupta', 'CSE', 'B', '', '', '', '9876543213'),
        (1, 'CSE-B-002', 'Vikram', 'Patel', 'CSE', 'B', '', '', '', '9876543214'),
        (1, 'CSE-B-003', 'Sneha', 'Reddy', 'CSE', 'B', '', '', '', '9876543215'),
        (1, 'CSE-C-001', 'Kiran', 'Kumar', 'CSE', 'C', '', '', '', '9876543216'),
        (1, 'CSE-C-002', 'Meera', 'Joshi', 'CSE', 'C', '', '', '', '9876543217'),
        (1, 'CSE-C-003', 'Arun', 'Verma', 'CSE', 'C', '', '', '', '9876543218'),
    ]
    
    for student in cse_students:
        cursor.execute('''
            INSERT OR IGNORE INTO students 
            (user_id, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals, mobile_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', student)
    
    print("Added CSE classes and students:")
    print("- CSE-A: 3 students")
    print("- CSE-B: 3 students") 
    print("- CSE-C: 3 students")
    print("- Total: 9 subjects across 3 CSE sections")
    
    conn.commit()
    conn.close()
    print("Database updated successfully!")

if __name__ == "__main__":
    add_cse_classes()