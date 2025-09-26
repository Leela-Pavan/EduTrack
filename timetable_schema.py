"""
Enhanced Database Schema for Automated Timetable Scheduling Module
This module extends the existing EduTrack database with comprehensive timetable management.
"""

from flask import Flask
import sqlite3
from datetime import datetime

def create_timetable_tables():
    """Create all tables required for the automated timetable scheduling system"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Enhanced Teachers table with qualifications and constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            teacher_code TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            subject_qualifications TEXT NOT NULL,  -- JSON array of subjects they can teach
            weekly_unavailability TEXT,  -- JSON: {"monday": ["09:00-10:00"], "friday": ["all_day"]}
            max_hours_per_week INTEGER DEFAULT 20,  -- Maximum 20 periods (45 min each) per week for EduTrack
            preferred_rooms TEXT,  -- JSON array of preferred room IDs
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Enhanced Subjects table with detailed requirements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            subject_type TEXT NOT NULL CHECK(subject_type IN ('theory', 'practical', 'lab', 'tutorial')),
            weekly_lecture_hours INTEGER NOT NULL DEFAULT 0,
            weekly_lab_hours INTEGER NOT NULL DEFAULT 0,
            weekly_tutorial_hours INTEGER NOT NULL DEFAULT 0,
            requires_special_room TEXT,  -- 'computer_lab', 'science_lab', 'auditorium', etc.
            min_room_capacity INTEGER DEFAULT 30,
            prerequisites TEXT,  -- JSON array of prerequisite subject IDs
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Enhanced Classrooms table with capacity and facilities
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_name TEXT NOT NULL,
            room_type TEXT NOT NULL CHECK(room_type IN ('lecture_hall', 'computer_lab', 'science_lab', 'tutorial_room', 'auditorium', 'workshop')),
            seating_capacity INTEGER NOT NULL,
            facilities TEXT,  -- JSON: {"projector": true, "computers": 30, "whiteboard": true}
            availability_constraints TEXT,  -- JSON: {"maintenance": ["monday_09:00-10:00"]}
            floor_number INTEGER,
            building_name TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Student Groups (Classes/Sections)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_student_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_code TEXT UNIQUE NOT NULL,  -- e.g., 'CSIT-A', 'CSD-B'
            group_name TEXT NOT NULL,  -- e.g., 'Computer Science IT - Section A'
            academic_year TEXT NOT NULL,  -- e.g., '2024-25'
            semester INTEGER NOT NULL,  -- 1, 2, 3, etc.
            student_count INTEGER NOT NULL,
            coordinator_teacher_id INTEGER,
            special_requirements TEXT,  -- JSON for any special scheduling needs
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coordinator_teacher_id) REFERENCES timetable_teachers (id)
        )
    ''')
    
    # Subject assignments to student groups
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            assigned_teacher_id INTEGER,
            weekly_hours INTEGER NOT NULL,
            session_type TEXT NOT NULL CHECK(session_type IN ('lecture', 'lab', 'tutorial', 'practical')),
            priority INTEGER DEFAULT 1,  -- Higher number = higher priority in scheduling
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES timetable_student_groups (id),
            FOREIGN KEY (subject_id) REFERENCES timetable_subjects (id),
            FOREIGN KEY (assigned_teacher_id) REFERENCES timetable_teachers (id),
            UNIQUE(group_id, subject_id, session_type)
        )
    ''')
    
    # Time Slots Definition
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_code TEXT UNIQUE NOT NULL,  -- e.g., 'MON_09_10', 'TUE_14_15'
            day_of_week TEXT NOT NULL CHECK(day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            slot_type TEXT NOT NULL CHECK(slot_type IN ('regular', 'lunch_break', 'short_break', 'lab_session')),
            duration_minutes INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Main Timetable Entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            academic_year TEXT NOT NULL,
            semester INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            time_slot_id INTEGER NOT NULL,
            session_type TEXT NOT NULL CHECK(session_type IN ('lecture', 'lab', 'tutorial', 'practical')),
            week_pattern TEXT DEFAULT 'all',  -- 'all', 'odd', 'even', 'specific'
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'cancelled', 'rescheduled', 'completed')),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER,  -- Admin user who created this entry
            FOREIGN KEY (group_id) REFERENCES timetable_student_groups (id),
            FOREIGN KEY (subject_id) REFERENCES timetable_subjects (id),
            FOREIGN KEY (teacher_id) REFERENCES timetable_teachers (id),
            FOREIGN KEY (classroom_id) REFERENCES timetable_classrooms (id),
            FOREIGN KEY (time_slot_id) REFERENCES time_slots (id),
            FOREIGN KEY (created_by) REFERENCES users (id),
            UNIQUE(group_id, time_slot_id, academic_year, semester),
            UNIQUE(teacher_id, time_slot_id, academic_year, semester),
            UNIQUE(classroom_id, time_slot_id, academic_year, semester)
        )
    ''')
    
    # Timetable Generation History and Settings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            academic_year TEXT NOT NULL,
            semester INTEGER NOT NULL,
            generation_method TEXT NOT NULL CHECK(generation_method IN ('auto', 'manual', 'hybrid')),
            constraints_used TEXT NOT NULL,  -- JSON of all constraints applied
            generation_status TEXT NOT NULL CHECK(generation_status IN ('in_progress', 'completed', 'failed', 'cancelled')),
            total_classes_scheduled INTEGER DEFAULT 0,
            conflicts_resolved INTEGER DEFAULT 0,
            generation_time_seconds REAL,
            success_rate REAL,  -- Percentage of requirements successfully scheduled
            generated_by INTEGER NOT NULL,
            generation_log TEXT,  -- Detailed log of the generation process
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (generated_by) REFERENCES users (id)
        )
    ''')
    
    # Conflict tracking for manual adjustments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable_conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            conflict_type TEXT NOT NULL CHECK(conflict_type IN ('teacher_double_booking', 'room_double_booking', 'group_double_booking', 'teacher_unavailable', 'room_unsuitable', 'capacity_exceeded')),
            conflict_description TEXT NOT NULL,
            severity TEXT NOT NULL CHECK(severity IN ('critical', 'major', 'minor', 'warning')),
            resolution_status TEXT DEFAULT 'unresolved' CHECK(resolution_status IN ('unresolved', 'resolved', 'ignored')),
            resolution_notes TEXT,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (entry_id) REFERENCES timetable_entries (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Timetable database schema created successfully!")

def insert_sample_time_slots():
    """Insert time slots for EduTrack: 9:00 AM - 4:30 PM with lunch break (12:00-1:30 PM), 4:30-5:30 PM curricular activities, Saturday half-day"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Clear existing time slots
    cursor.execute('DELETE FROM time_slots')
    
    # Time slots for weekdays (Monday-Friday): 9:00 AM - 4:30 PM with lunch break
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = []
    
    for day in weekdays:
        # Morning Session: 9:00 AM - 12:15 PM (4 periods of 45 minutes each)
        time_slots.extend([
            (f"{day.upper()[:3]}_0900_0945", day, '09:00', '09:45', 'academic', 45),
            (f"{day.upper()[:3]}_0945_1030", day, '09:45', '10:30', 'academic', 45),
            (f"{day.upper()[:3]}_1030_1045", day, '10:30', '10:45', 'short_break', 15),
            (f"{day.upper()[:3]}_1045_1130", day, '10:45', '11:30', 'academic', 45),
            (f"{day.upper()[:3]}_1130_1215", day, '11:30', '12:15', 'academic', 45),
            
            # Lunch Break: 12:15 PM - 1:30 PM (75 minutes)
            (f"{day.upper()[:3]}_1215_1330", day, '12:15', '13:30', 'lunch_break', 75),
            
            # Afternoon Session: 1:30 PM - 4:45 PM (4 periods of 45 minutes each)
            (f"{day.upper()[:3]}_1330_1415", day, '13:30', '14:15', 'academic', 45),
            (f"{day.upper()[:3]}_1415_1500", day, '14:15', '15:00', 'academic', 45),
            (f"{day.upper()[:3]}_1500_1515", day, '15:00', '15:15', 'short_break', 15),
            (f"{day.upper()[:3]}_1515_1600", day, '15:15', '16:00', 'academic', 45),
            (f"{day.upper()[:3]}_1600_1645", day, '16:00', '16:45', 'academic', 45),
            
            # Curricular Activities: 4:45 PM - 5:30 PM (45 minutes)
            (f"{day.upper()[:3]}_1645_1730", day, '16:45', '17:30', 'extra_curricular', 45),
        ])
    
    # Saturday (Half Day): 9:00 AM - 1:00 PM (4 periods of 45 minutes each)
    time_slots.extend([
        ('SAT_0900_0945', 'Saturday', '09:00', '09:45', 'academic', 45),
        ('SAT_0945_1030', 'Saturday', '09:45', '10:30', 'academic', 45),
        ('SAT_1030_1045', 'Saturday', '10:30', '10:45', 'short_break', 15),
        ('SAT_1045_1130', 'Saturday', '10:45', '11:30', 'academic', 45),
        ('SAT_1130_1215', 'Saturday', '11:30', '12:15', 'academic', 45),
        ('SAT_1215_1300', 'Saturday', '12:15', '13:00', 'extended_break', 45),
    ])
    
    # Sunday is a holiday - no time slots
    
    # Insert all time slots
    for slot_data in time_slots:
        cursor.execute('''
            INSERT OR IGNORE INTO time_slots 
            (slot_code, day_of_week, start_time, end_time, slot_type, duration_minutes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', slot_data)
    
    conn.commit()
    conn.close()
    print("✅ EduTrack time slots (9:00 AM - 4:30 PM with lunch break, Saturday half-day) inserted successfully!")

if __name__ == '__main__':
    create_timetable_tables()
    insert_sample_time_slots()