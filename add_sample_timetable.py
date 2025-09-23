#!/usr/bin/env python3

import sqlite3
from datetime import datetime

def add_sample_timetable_data():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # First, check if we have the teacher Raju (ID 101)
    cursor.execute('SELECT teacher_id FROM teachers WHERE teacher_id = ?', (101,))
    teacher = cursor.fetchone()
    
    if not teacher:
        print("Teacher Raju (ID 101) not found. Please register first.")
        conn.close()
        return
    
    # Add some sample classes for teacher 101 (Raju)
    # Let's add classes for today (whatever day it is)
    today = datetime.now().strftime('%A')
    
    print(f"Adding sample timetable for teacher 101 (Raju) for {today}")
    
    # Clear existing timetable for this teacher
    cursor.execute('DELETE FROM timetable WHERE teacher_id = ?', (101,))
    
    # Add sample timetable entries
    timetable_data = [
        (101, '11', 'A', today, 1, 'DLCO', '09:00', '10:00'),
        (101, '11', 'B', today, 3, 'DLCO', '11:00', '12:00'),
        (101, '12', 'A', today, 5, 'DLCO', '14:00', '15:00'),
    ]
    
    cursor.executemany('''INSERT INTO timetable 
                         (teacher_id, class_name, section, day_of_week, period_number, subject, start_time, end_time)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', timetable_data)
    
    # Also add some classes for other days to make it realistic
    other_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day in other_days:
        if day != today:
            cursor.execute('''INSERT INTO timetable 
                             (teacher_id, class_name, section, day_of_week, period_number, subject, start_time, end_time)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (101, '11', 'A', day, 2, 'DLCO', '10:00', '11:00'))
    
    conn.commit()
    
    # Verify the data was added
    cursor.execute('SELECT * FROM timetable WHERE teacher_id = ?', (101,))
    classes = cursor.fetchall()
    
    print(f"Added {len(classes)} timetable entries for teacher 101:")
    for class_info in classes:
        print(f"  {class_info[3]} - Period {class_info[4]}: {class_info[5]} for Class {class_info[1]}-{class_info[2]}")
    
    conn.close()
    print("Sample timetable data added successfully!")

if __name__ == '__main__':
    add_sample_timetable_data()