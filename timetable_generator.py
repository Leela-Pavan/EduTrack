"""
Automated Timetable Generation Engine
This module implements a constraint-based algorithm for generating conflict-free timetables.
Uses techniques like constraint satisfaction, backtracking, and heuristic optimization.
"""

import sqlite3
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class TimeSlot:
    """Represents a time slot in the timetable"""
    id: int
    day: str
    start_time: str
    end_time: str
    duration: int
    slot_code: str
    slot_type: str = 'academic'  # academic, break, lunch_break, extra_curricular

@dataclass
class Teacher:
    """Represents a teacher with constraints"""
    id: int
    code: str
    name: str
    qualifications: List[str]
    max_hours: int
    unavailability: Dict[str, List[str]]
    
@dataclass
class Subject:
    """Represents a subject with requirements"""
    id: int
    code: str
    name: str
    subject_type: str
    lecture_hours: int
    lab_hours: int
    tutorial_hours: int
    special_room: Optional[str]
    min_capacity: int

@dataclass
class Classroom:
    """Represents a classroom with facilities"""
    id: int
    number: str
    name: str
    room_type: str
    capacity: int
    facilities: Dict[str, bool]

@dataclass
class StudentGroup:
    """Represents a student group/class"""
    id: int
    code: str
    name: str
    student_count: int
    coordinator_id: Optional[int]

@dataclass
class ClassSession:
    """Represents a single class session to be scheduled"""
    id: str
    group_id: int
    subject_id: int
    teacher_id: int
    session_type: str  # 'lecture', 'lab', 'tutorial'
    duration: int
    required_room_type: Optional[str]
    min_capacity: int
    
    # Assigned values (to be filled during scheduling)
    classroom_id: Optional[int] = None
    time_slot_id: Optional[int] = None
    day: Optional[str] = None
    start_time: Optional[str] = None

class Constraint:
    """Base class for scheduling constraints"""
    def __init__(self, name: str, severity: str = 'critical'):
        self.name = name
        self.severity = severity  # 'critical', 'major', 'minor', 'warning'
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        """Check if the constraint is satisfied. Returns (is_satisfied, reason)"""
        raise NotImplementedError

class NoDoubleBookingConstraint(Constraint):
    """Ensures no teacher, room, or group is double-booked"""
    def __init__(self):
        super().__init__("No Double Booking", "critical")
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        if not session.time_slot_id or not session.classroom_id:
            return True, ""
        
        time_slot_id = session.time_slot_id
        
        # Check for conflicts with already scheduled sessions
        for scheduled_id, scheduled_session in assignments.items():
            if scheduled_id == session.id:
                continue
                
            if scheduled_session.time_slot_id == time_slot_id:
                # Same time slot - check for conflicts
                
                # Teacher conflict
                if scheduled_session.teacher_id == session.teacher_id:
                    return False, f"Teacher double-booked at time slot {time_slot_id}"
                
                # Classroom conflict
                if scheduled_session.classroom_id == session.classroom_id:
                    return False, f"Classroom {session.classroom_id} double-booked at time slot {time_slot_id}"
                
                # Student group conflict
                if scheduled_session.group_id == session.group_id:
                    return False, f"Student group {session.group_id} double-booked at time slot {time_slot_id}"
        
        return True, ""

class TeacherAvailabilityConstraint(Constraint):
    """Ensures teachers are scheduled only when available"""
    def __init__(self):
        super().__init__("Teacher Availability", "critical")
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        if not session.time_slot_id or not session.teacher_id:
            return True, ""
        
        teacher = data['teachers'].get(session.teacher_id)
        time_slot = data['time_slots'].get(session.time_slot_id)
        
        if not teacher or not time_slot:
            return True, ""
        
        # Check teacher unavailability
        unavailability = teacher.unavailability
        day = time_slot.day.lower()
        
        if day in unavailability:
            unavailable_slots = unavailability[day]
            
            # Check if teacher is unavailable all day
            if 'all_day' in unavailable_slots:
                return False, f"Teacher {teacher.name} is unavailable on {day}"
            
            # Check specific time slots
            for slot in unavailable_slots:
                if slot in ['morning', 'afternoon']:
                    # Implementation for morning/afternoon checks
                    slot_hour = int(time_slot.start_time.split(':')[0])
                    if slot == 'morning' and 9 <= slot_hour < 12:
                        return False, f"Teacher {teacher.name} is unavailable in the morning on {day}"
                    elif slot == 'afternoon' and 14 <= slot_hour < 17:
                        return False, f"Teacher {teacher.name} is unavailable in the afternoon on {day}"
        
        return True, ""

class RoomSuitabilityConstraint(Constraint):
    """Ensures rooms meet subject requirements"""
    def __init__(self):
        super().__init__("Room Suitability", "major")
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        if not session.classroom_id or not session.subject_id:
            return True, ""
        
        classroom = data['classrooms'].get(session.classroom_id)
        subject = data['subjects'].get(session.subject_id)
        group = data['groups'].get(session.group_id)
        
        if not classroom or not subject or not group:
            return True, ""
        
        # Check capacity
        if classroom.capacity < group.student_count:
            return False, f"Classroom {classroom.name} capacity ({classroom.capacity}) insufficient for group size ({group.student_count})"
        
        # Check special room requirements
        if subject.special_room:
            required_type = subject.special_room.replace('_', '')
            room_type = classroom.room_type.replace('_', '')
            
            if required_type not in room_type:
                return False, f"Subject {subject.name} requires {subject.special_room} but classroom {classroom.name} is {classroom.room_type}"
        
        return True, ""

class TeacherQualificationConstraint(Constraint):
    """Ensures teachers are qualified for assigned subjects"""
    def __init__(self):
        super().__init__("Teacher Qualification", "critical")
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        if not session.teacher_id or not session.subject_id:
            return True, ""
        
        teacher = data['teachers'].get(session.teacher_id)
        subject = data['subjects'].get(session.subject_id)
        
        if not teacher or not subject:
            return True, ""
        
        # Check if teacher is qualified for the subject
        if subject.code not in teacher.qualifications:
            return False, f"Teacher {teacher.name} is not qualified to teach {subject.name}"
        
        return True, ""

class WorkloadConstraint(Constraint):
    """Ensures teachers don't exceed maximum weekly periods (EduTrack: 20 periods of 45 min each)"""
    def __init__(self):
        super().__init__("Teacher Workload", "major")
    
    def check(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, str]:
        if not session.teacher_id:
            return True, ""
        
        teacher = data['teachers'].get(session.teacher_id)
        if not teacher:
            return True, ""
        
        # Count current weekly academic periods for this teacher (excluding breaks)
        weekly_periods = 0
        for scheduled_session in assignments.values():
            if (scheduled_session.teacher_id == session.teacher_id and
                hasattr(scheduled_session, 'time_slot_type') and
                scheduled_session.time_slot_type == 'academic'):
                weekly_periods += 1
        
        # EduTrack specific: Maximum 20 academic periods (45 min each) per week
        max_periods = min(teacher.max_hours, 20)  # Enforce 20-period limit for EduTrack
        
        if weekly_periods >= max_periods:
            return False, f"Teacher {teacher.name} would exceed maximum weekly periods ({max_periods})"
        
        return True, ""

class TimetableGenerator:
    """Main timetable generation engine"""
    
    def __init__(self):
        self.constraints = [
            NoDoubleBookingConstraint(),
            TeacherAvailabilityConstraint(),
            TeacherQualificationConstraint(),
            RoomSuitabilityConstraint(),
            WorkloadConstraint()
        ]
        
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect('school_system.db')
        conn.row_factory = sqlite3.Row
        return conn
    
    def load_data(self, academic_year: str, semester: int) -> Dict:
        """Load all necessary data for timetable generation"""
        conn = self.get_db_connection()
        
        data = {
            'teachers': {},
            'subjects': {},
            'classrooms': {},
            'groups': {},
            'time_slots': {},
            'group_subjects': []
        }
        
        try:
            # Load teachers
            teachers = conn.execute('SELECT * FROM timetable_teachers').fetchall()
            for teacher in teachers:
                data['teachers'][teacher['id']] = Teacher(
                    id=teacher['id'],
                    code=teacher['teacher_code'],
                    name=f"{teacher['first_name']} {teacher['last_name']}",
                    qualifications=json.loads(teacher['subject_qualifications'] or '[]'),
                    max_hours=teacher['max_hours_per_week'],
                    unavailability=json.loads(teacher['weekly_unavailability'] or '{}')
                )
            
            # Load subjects
            subjects = conn.execute('SELECT * FROM timetable_subjects').fetchall()
            for subject in subjects:
                data['subjects'][subject['id']] = Subject(
                    id=subject['id'],
                    code=subject['subject_code'],
                    name=subject['subject_name'],
                    subject_type=subject['subject_type'],
                    lecture_hours=subject['weekly_lecture_hours'],
                    lab_hours=subject['weekly_lab_hours'],
                    tutorial_hours=subject['weekly_tutorial_hours'],
                    special_room=subject['requires_special_room'],
                    min_capacity=subject['min_room_capacity']
                )
            
            # Load classrooms
            classrooms = conn.execute('SELECT * FROM timetable_classrooms WHERE is_active = 1').fetchall()
            for classroom in classrooms:
                data['classrooms'][classroom['id']] = Classroom(
                    id=classroom['id'],
                    number=classroom['room_number'],
                    name=classroom['room_name'],
                    room_type=classroom['room_type'],
                    capacity=classroom['seating_capacity'],
                    facilities=json.loads(classroom['facilities'] or '{}')
                )
            
            # Load student groups
            groups = conn.execute('SELECT * FROM timetable_student_groups').fetchall()
            for group in groups:
                data['groups'][group['id']] = StudentGroup(
                    id=group['id'],
                    code=group['group_code'],
                    name=group['group_name'],
                    student_count=group['student_count'],
                    coordinator_id=group['coordinator_teacher_id']
                )
            
            # Load time slots - only academic periods for EduTrack scheduling
            time_slots = conn.execute('''
                SELECT * FROM time_slots 
                WHERE slot_type = 'academic' 
                ORDER BY day_of_week, start_time
            ''').fetchall()
            for slot in time_slots:
                data['time_slots'][slot['id']] = TimeSlot(
                    id=slot['id'],
                    day=slot['day_of_week'],
                    start_time=slot['start_time'],
                    end_time=slot['end_time'],
                    duration=slot['duration_minutes'],
                    slot_code=slot['slot_code'],
                    slot_type=slot['slot_type']
                )
            
            # Load group-subject assignments
            group_subjects = conn.execute('''
                SELECT gs.*, s.subject_code, s.subject_name, s.subject_type
                FROM group_subjects gs
                JOIN timetable_subjects s ON gs.subject_id = s.id
                JOIN timetable_student_groups g ON gs.group_id = g.id
                WHERE g.academic_year = ? AND g.semester = ?
            ''', (academic_year, semester)).fetchall()
            
            data['group_subjects'] = [dict(gs) for gs in group_subjects]
            
        finally:
            conn.close()
        
        return data
    
    def create_class_sessions(self, data: Dict) -> List[ClassSession]:
        """Create all class sessions that need to be scheduled"""
        sessions = []
        session_id = 0
        
        for gs in data['group_subjects']:
            group_id = gs['group_id']
            subject_id = gs['subject_id']
            teacher_id = gs['assigned_teacher_id']
            weekly_hours = gs['weekly_hours']
            session_type = gs['session_type']
            
            if not teacher_id:
                continue  # Skip unassigned subjects
            
            subject = data['subjects'].get(subject_id)
            if not subject:
                continue
            
            # Calculate number of sessions needed
            session_duration = 60  # Default 1 hour sessions
            if session_type == 'lab':
                session_duration = 120  # 2-hour lab sessions
            elif session_type == 'tutorial':
                session_duration = 60   # 1-hour tutorials
            
            num_sessions = (weekly_hours * 60) // session_duration
            
            # Create sessions
            for i in range(num_sessions):
                session_id += 1
                session = ClassSession(
                    id=f"{group_id}_{subject_id}_{session_type}_{i+1}",
                    group_id=group_id,
                    subject_id=subject_id,
                    teacher_id=teacher_id,
                    session_type=session_type,
                    duration=session_duration,
                    required_room_type=subject.special_room,
                    min_capacity=subject.min_capacity
                )
                sessions.append(session)
        
        return sessions
    
    def get_domain_values(self, session: ClassSession, data: Dict) -> Dict:
        """Get possible values for each variable (time_slot, classroom)"""
        domain = {
            'time_slots': list(data['time_slots'].keys()),
            'classrooms': []
        }
        
        # Filter classrooms based on requirements
        subject = data['subjects'].get(session.subject_id)
        group = data['groups'].get(session.group_id)
        
        for classroom_id, classroom in data['classrooms'].items():
            # Check capacity
            if group and classroom.capacity >= group.student_count:
                # Check room type if special room required
                if subject and subject.special_room:
                    if subject.special_room.replace('_', '') in classroom.room_type.replace('_', ''):
                        domain['classrooms'].append(classroom_id)
                else:
                    domain['classrooms'].append(classroom_id)
        
        return domain
    
    def check_constraints(self, session: ClassSession, assignments: Dict, data: Dict) -> Tuple[bool, List[str]]:
        """Check all constraints for a given assignment"""
        violations = []
        all_satisfied = True
        
        for constraint in self.constraints:
            satisfied, reason = constraint.check(session, assignments, data)
            if not satisfied:
                all_satisfied = False
                violations.append(f"{constraint.name}: {reason}")
        
        return all_satisfied, violations
    
    def select_unassigned_variable(self, sessions: List[ClassSession]) -> Optional[ClassSession]:
        """Select the next session to schedule using MRV (Most Remaining Values) heuristic"""
        unassigned = [s for s in sessions if s.time_slot_id is None or s.classroom_id is None]
        
        if not unassigned:
            return None
        
        # Use degree heuristic - pick sessions with most constraints first
        priority_sessions = []
        for session in unassigned:
            priority = 0
            
            # Higher priority for lab sessions (longer duration)
            if session.session_type == 'lab':
                priority += 2
            
            # Higher priority for subjects with special room requirements
            if session.required_room_type:
                priority += 3
            
            priority_sessions.append((priority, session))
        
        # Sort by priority (descending) and return the highest priority session
        priority_sessions.sort(key=lambda x: x[0], reverse=True)
        return priority_sessions[0][1]
    
    def backtrack_search(self, sessions: List[ClassSession], assignments: Dict, data: Dict) -> bool:
        """Backtracking search algorithm for scheduling"""
        session = self.select_unassigned_variable(sessions)
        
        if session is None:
            return True  # All sessions assigned successfully
        
        # Get domain values
        domain = self.get_domain_values(session, data)
        
        # Try all combinations of time slot and classroom
        time_slots = list(domain['time_slots'])
        classrooms = list(domain['classrooms'])
        
        # Randomize to avoid always getting the same solution
        random.shuffle(time_slots)
        random.shuffle(classrooms)
        
        for time_slot_id in time_slots:
            for classroom_id in classrooms:
                # Assign values
                session.time_slot_id = time_slot_id
                session.classroom_id = classroom_id
                
                time_slot = data['time_slots'].get(time_slot_id)
                if time_slot:
                    session.day = time_slot.day
                    session.start_time = time_slot.start_time
                
                # Check constraints
                satisfied, violations = self.check_constraints(session, assignments, data)
                
                if satisfied:
                    # Add to assignments
                    assignments[session.id] = session
                    
                    # Recursively try to assign remaining sessions
                    if self.backtrack_search(sessions, assignments, data):
                        return True
                    
                    # Backtrack - remove assignment
                    del assignments[session.id]
                
                # Remove values for next iteration
                session.time_slot_id = None
                session.classroom_id = None
                session.day = None
                session.start_time = None
        
        return False  # No valid assignment found
    
    def save_timetable(self, assignments: Dict, academic_year: str, semester: int, admin_user_id: int) -> Dict:
        """Save the generated timetable to database"""
        conn = self.get_db_connection()
        
        try:
            # Clear existing timetable for this academic year and semester
            conn.execute('''
                DELETE FROM timetable_entries 
                WHERE academic_year = ? AND semester = ?
            ''', (academic_year, semester))
            
            # Insert new timetable entries
            total_classes = 0
            for session_id, session in assignments.items():
                if session.time_slot_id and session.classroom_id:
                    conn.execute('''
                        INSERT INTO timetable_entries
                        (academic_year, semester, group_id, subject_id, teacher_id, 
                         classroom_id, time_slot_id, session_type, status, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        academic_year, semester, session.group_id, session.subject_id,
                        session.teacher_id, session.classroom_id, session.time_slot_id,
                        session.session_type, 'active', admin_user_id
                    ))
                    total_classes += 1
            
            # Record generation metadata
            generation_cursor = conn.execute('''
                INSERT INTO timetable_generations
                (academic_year, semester, generation_method, constraints_used, 
                 generation_status, total_classes_scheduled, generated_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                academic_year, semester, 'auto', 
                json.dumps([c.name for c in self.constraints]),
                'completed', total_classes, admin_user_id
            ))
            
            generation_id = generation_cursor.lastrowid
            conn.commit()
            
            return {
                'success': True,
                'total_classes': total_classes,
                'generation_id': generation_id
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            conn.close()
    
    def generate_timetable(self, academic_year: str = '2024-25', semester: int = 1, 
                          method: str = 'auto', admin_user_id: int = 1) -> Dict:
        """Main timetable generation method"""
        start_time = time.time()
        
        try:
            # Load all data
            data = self.load_data(academic_year, semester)
            
            # Create sessions to be scheduled
            sessions = self.create_class_sessions(data)
            
            if not sessions:
                return {
                    'success': False,
                    'error': 'No sessions to schedule. Please ensure subjects are assigned to student groups.'
                }
            
            # Use backtracking search to find solution
            assignments = {}
            success = self.backtrack_search(sessions, assignments, data)
            
            generation_time = time.time() - start_time
            
            if success:
                # Save timetable to database
                save_result = self.save_timetable(assignments, academic_year, semester, admin_user_id)
                
                if save_result['success']:
                    success_rate = (len(assignments) / len(sessions)) * 100
                    
                    # Update generation record with timing info
                    conn = self.get_db_connection()
                    conn.execute('''
                        UPDATE timetable_generations 
                        SET generation_time_seconds = ?, success_rate = ?
                        WHERE id = ?
                    ''', (generation_time, success_rate, save_result['generation_id']))
                    conn.commit()
                    conn.close()
                    
                    return {
                        'success': True,
                        'total_classes': save_result['total_classes'],
                        'success_rate': round(success_rate, 2),
                        'generation_id': save_result['generation_id'],
                        'generation_time': round(generation_time, 2)
                    }
                else:
                    return save_result
            else:
                return {
                    'success': False,
                    'error': 'Could not generate a conflict-free timetable with current constraints. Please review teacher availability and room requirements.',
                    'generation_time': round(generation_time, 2)
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Generation failed: {str(e)}',
                'generation_time': round(time.time() - start_time, 2)
            }