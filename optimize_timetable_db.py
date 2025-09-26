"""
Database optimization script for EduTrack Timetable System
Adds indexes and optimizes queries for better performance
"""

import sqlite3

def optimize_timetable_database():
    """Add indexes to improve query performance"""
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("🚀 Optimizing EduTrack Timetable Database...")
    
    # Create indexes for frequently queried columns
    indexes = [
        # Timetable entries - main performance bottleneck
        ('idx_timetable_entries_academic', 'timetable_entries', 'academic_year, semester, status'),
        ('idx_timetable_entries_teacher', 'timetable_entries', 'teacher_id, status'),
        ('idx_timetable_entries_group', 'timetable_entries', 'group_id, status'),
        ('idx_timetable_entries_classroom', 'timetable_entries', 'classroom_id, status'),
        ('idx_timetable_entries_timeslot', 'timetable_entries', 'time_slot_id, status'),
        
        # Time slots for ordering and filtering
        ('idx_time_slots_day_time', 'time_slots', 'day_of_week, start_time'),
        ('idx_time_slots_type', 'time_slots', 'slot_type'),
        
        # Teachers for lookups
        ('idx_teachers_code', 'timetable_teachers', 'teacher_code'),
        ('idx_teachers_active', 'timetable_teachers', 'is_active'),
        
        # Subjects for lookups
        ('idx_subjects_code', 'timetable_subjects', 'subject_code'),
        
        # Classrooms for lookups
        ('idx_classrooms_active', 'timetable_classrooms', 'is_active'),
        ('idx_classrooms_type', 'timetable_classrooms', 'room_type, is_active'),
        
        # Student groups for lookups
        ('idx_groups_code', 'timetable_student_groups', 'group_code'),
        ('idx_groups_year_sem', 'timetable_student_groups', 'academic_year, semester'),
        
        # Conflicts for quick resolution
        ('idx_conflicts_status', 'timetable_conflicts', 'resolution_status'),
        ('idx_conflicts_entry', 'timetable_conflicts', 'entry_id, resolution_status'),
    ]
    
    created_count = 0
    for index_name, table_name, columns in indexes:
        try:
            cursor.execute(f'''
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON {table_name} ({columns})
            ''')
            created_count += 1
            print(f"✅ Created index: {index_name}")
        except sqlite3.Error as e:
            print(f"⚠️  Warning creating {index_name}: {e}")
    
    # Optimize database
    cursor.execute('ANALYZE')
    cursor.execute('VACUUM')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database optimization completed! Created {created_count} indexes")
    print("📊 Run EXPLAIN QUERY PLAN to verify query performance improvements")

if __name__ == '__main__':
    optimize_timetable_database()