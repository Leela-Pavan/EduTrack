#!/usr/bin/env python3
"""
Set CSIT-A schedule as per user specifications
"""
import sqlite3

def set_csit_a_schedule():
    print("📅 Setting CSIT-A Schedule...")
    
    # Schedule data from user specification
    schedule_data = [
        # Monday
        ("Monday", "09:00", "10:00", "JAVA (AKV)", "U-407"),
        ("Monday", "10:00", "11:00", "EP", "U-407"),
        ("Monday", "11:00", "12:00", "DMGT (NVR)", "U-407"),
        ("Monday", "12:00", "13:00", "", ""),  # Empty slot
        ("Monday", "13:00", "14:00", "Sports/Yoga", ""),
        ("Monday", "14:00", "15:00", "Sports/Yoga", ""),
        
        # Tuesday
        ("Tuesday", "09:00", "10:00", "DLCO (JTR)", "TC"),
        ("Tuesday", "10:00", "11:00", "DBMS (NGKM)", "TC"),
        ("Tuesday", "11:00", "12:00", "PYTHON LAB", "Lab-1"),
        ("Tuesday", "12:00", "13:00", "DBMS LAB", "Lab-1"),
        ("Tuesday", "13:00", "14:00", "Sports/Yoga", ""),
        ("Tuesday", "14:00", "15:00", "Sports/Yoga", ""),
        
        # Wednesday
        ("Wednesday", "09:00", "10:00", "Placement Training", "U-407"),
        
        # Thursday
        ("Thursday", "09:00", "10:00", "DBMS (NGKM)", "TC"),
        ("Thursday", "10:00", "11:00", "UHV-II", "TC"),
        
        # Friday
        ("Friday", "09:00", "10:00", "UHV-II", "TC"),
        ("Friday", "10:00", "11:00", "DMGT", "U-407"),
        ("Friday", "11:00", "12:00", "JAVA LAB", "Lab-1"),
        ("Friday", "12:00", "13:00", "Sports/Yoga", ""),
        ("Friday", "13:00", "14:00", "Sports/Yoga", ""),
        
        # Saturday
        ("Saturday", "09:00", "10:00", "JAVA (AKV)", "TC"),
        ("Saturday", "10:00", "11:00", "DLCO (JTR)", "TC"),
    ]
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # First, delete existing CSIT-A schedule
        print("1. Removing existing CSIT-A schedule...")
        cursor.execute("DELETE FROM timetable WHERE class_name = 'CSIT' AND section = 'A'")
        deleted_count = cursor.rowcount
        print(f"   ✅ Removed {deleted_count} existing entries")
        
        # Insert new schedule
        print("\n2. Inserting new CSIT-A schedule...")
        inserted_count = 0
        
        for day, start_time, end_time, subject, room in schedule_data:
            # Skip empty subjects (lunch breaks, etc.)
            if not subject.strip():
                continue
                
            # Determine period number based on start time
            time_to_period = {
                "09:00": 1,
                "10:00": 2,
                "11:00": 3,
                "12:00": 4,
                "13:00": 5,
                "14:00": 6,
                "15:00": 7,
                "16:00": 8
            }
            
            period_number = time_to_period.get(start_time, 1)
            
            # Try to find teacher from subject string (e.g., "JAVA (AKV)" -> find teacher AKV)
            teacher_id = None
            if "(" in subject and ")" in subject:
                # Extract teacher code from subject (e.g., "JAVA (AKV)" -> "AKV")
                teacher_code = subject[subject.find("(")+1:subject.find(")")]
                
                # Try to find teacher by username or name containing the code
                cursor.execute('''
                    SELECT t.user_id FROM teachers t 
                    LEFT JOIN users u ON t.user_id = u.id
                    WHERE LOWER(u.username) LIKE LOWER(?) 
                    OR LOWER(t.first_name) LIKE LOWER(?)
                    OR LOWER(t.last_name) LIKE LOWER(?)
                    LIMIT 1
                ''', (f'%{teacher_code}%', f'%{teacher_code}%', f'%{teacher_code}%'))
                
                teacher_result = cursor.fetchone()
                if teacher_result:
                    teacher_id = teacher_result[0]
            
            # Insert schedule entry (room info will be part of subject)
            subject_with_room = f"{subject} - {room}" if room and room.strip() else subject
            cursor.execute('''
                INSERT INTO timetable 
                (class_name, section, day_of_week, period_number, subject, teacher_id, start_time, end_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("CSIT", "A", day, period_number, subject_with_room, teacher_id, start_time, end_time))
            
            inserted_count += 1
            teacher_name = "Unassigned" if not teacher_id else "Assigned"
            print(f"   ✅ {day} {start_time}-{end_time}: {subject_with_room} - {teacher_name}")
        
        conn.commit()
        conn.close()
        
        print(f"\n3. ✅ Schedule update completed!")
        print(f"   📊 Inserted {inserted_count} schedule entries for CSIT-A")
        
        # Verify the schedule
        print(f"\n4. Verifying CSIT-A schedule...")
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT day_of_week, start_time, end_time, subject
            FROM timetable 
            WHERE class_name = 'CSIT' AND section = 'A'
            ORDER BY 
                CASE day_of_week 
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2 
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    ELSE 7
                END,
                start_time
        ''')
        
        schedule_entries = cursor.fetchall()
        
        print(f"   📋 CSIT-A Schedule Summary ({len(schedule_entries)} entries):")
        current_day = ""
        for day, start, end, subject in schedule_entries:
            if day != current_day:
                print(f"\n   {day}:")
                current_day = day
            print(f"      {start}-{end}: {subject}")
        
        conn.close()
        
        print(f"\n" + "="*60)
        print(f"🎉 CSIT-A SCHEDULE SET SUCCESSFULLY!")
        print(f"="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    set_csit_a_schedule()