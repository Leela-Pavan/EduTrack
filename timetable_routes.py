"""
Timetable Management API Routes
This module provides all API endpoints for the automated timetable scheduling system.
"""

from flask import Blueprint, request, jsonify, session
import sqlite3
import json
from datetime import datetime
from functools import wraps

# Create blueprint for timetable management
timetable_bp = Blueprint('timetable', __name__, url_prefix='/api/timetable')

def require_admin(f):
    """Decorator to ensure only admin users can access timetable management"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect('school_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# Teachers API
@timetable_bp.route('/teachers', methods=['GET'])
@require_admin
def get_teachers():
    """Get all teachers with their details"""
    try:
        conn = get_db_connection()
        teachers = conn.execute('''
            SELECT * FROM timetable_teachers 
            WHERE user_id IS NOT NULL
            ORDER BY first_name, last_name
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(teacher) for teacher in teachers])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/teachers', methods=['POST'])
@require_admin
def create_teacher():
    """Create a new teacher"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['teacher_code', 'first_name', 'last_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        
        # Check if teacher code already exists
        existing = conn.execute(
            'SELECT id FROM timetable_teachers WHERE teacher_code = ?',
            (data['teacher_code'],)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'error': 'Teacher code already exists'}), 400
        
        # Insert new teacher
        cursor = conn.execute('''
            INSERT INTO timetable_teachers 
            (teacher_code, first_name, last_name, email, phone, subject_qualifications, 
             weekly_unavailability, max_hours_per_week)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['teacher_code'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone', ''),
            data.get('subject_qualifications', '[]'),
            data.get('weekly_unavailability', '{}'),
            data.get('max_hours_per_week', 40)
        ))
        
        teacher_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': teacher_id, 'message': 'Teacher created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
@require_admin
def update_teacher(teacher_id):
    """Update an existing teacher"""
    try:
        data = request.get_json()
        conn = get_db_connection()
        
        # Check if teacher exists
        teacher = conn.execute(
            'SELECT id FROM timetable_teachers WHERE id = ?',
            (teacher_id,)
        ).fetchone()
        
        if not teacher:
            conn.close()
            return jsonify({'error': 'Teacher not found'}), 404
        
        # Update teacher
        conn.execute('''
            UPDATE timetable_teachers 
            SET first_name = ?, last_name = ?, email = ?, phone = ?, 
                subject_qualifications = ?, weekly_unavailability = ?, 
                max_hours_per_week = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('first_name'),
            data.get('last_name'),
            data.get('email'),
            data.get('phone', ''),
            data.get('subject_qualifications', '[]'),
            data.get('weekly_unavailability', '{}'),
            data.get('max_hours_per_week', 40),
            teacher_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Teacher updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
@require_admin
def delete_teacher(teacher_id):
    """Delete a teacher"""
    try:
        conn = get_db_connection()
        
        # Check if teacher exists
        teacher = conn.execute(
            'SELECT id FROM timetable_teachers WHERE id = ?',
            (teacher_id,)
        ).fetchone()
        
        if not teacher:
            conn.close()
            return jsonify({'error': 'Teacher not found'}), 404
        
        # Check if teacher is assigned to any classes
        assignments = conn.execute(
            'SELECT COUNT(*) as count FROM timetable_entries WHERE teacher_id = ?',
            (teacher_id,)
        ).fetchone()
        
        if assignments['count'] > 0:
            conn.close()
            return jsonify({'error': 'Cannot delete teacher with existing class assignments'}), 400
        
        # Delete teacher
        conn.execute('DELETE FROM timetable_teachers WHERE id = ?', (teacher_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Teacher deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Subjects API
@timetable_bp.route('/subjects', methods=['GET'])
@require_admin
def get_subjects():
    """Get all subjects"""
    try:
        conn = get_db_connection()
        subjects = conn.execute('''
            SELECT * FROM timetable_subjects 
            ORDER BY subject_name
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(subject) for subject in subjects])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/subjects', methods=['POST'])
@require_admin
def create_subject():
    """Create a new subject"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['subject_code', 'subject_name', 'subject_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        
        # Check if subject code already exists
        existing = conn.execute(
            'SELECT id FROM timetable_subjects WHERE subject_code = ?',
            (data['subject_code'],)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'error': 'Subject code already exists'}), 400
        
        # Insert new subject
        cursor = conn.execute('''
            INSERT INTO timetable_subjects 
            (subject_code, subject_name, subject_type, weekly_lecture_hours, 
             weekly_lab_hours, weekly_tutorial_hours, requires_special_room, 
             min_room_capacity, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['subject_code'],
            data['subject_name'],
            data['subject_type'],
            data.get('weekly_lecture_hours', 0),
            data.get('weekly_lab_hours', 0),
            data.get('weekly_tutorial_hours', 0),
            data.get('requires_special_room'),
            data.get('min_room_capacity', 30),
            data.get('description', '')
        ))
        
        subject_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': subject_id, 'message': 'Subject created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Classrooms API
@timetable_bp.route('/classrooms', methods=['GET'])
@require_admin
def get_classrooms():
    """Get all classrooms"""
    try:
        conn = get_db_connection()
        classrooms = conn.execute('''
            SELECT * FROM timetable_classrooms 
            WHERE is_active = 1
            ORDER BY room_number
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(classroom) for classroom in classrooms])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/classrooms', methods=['POST'])
@require_admin
def create_classroom():
    """Create a new classroom"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['room_number', 'room_name', 'room_type', 'seating_capacity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        
        # Check if room number already exists
        existing = conn.execute(
            'SELECT id FROM timetable_classrooms WHERE room_number = ?',
            (data['room_number'],)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'error': 'Room number already exists'}), 400
        
        # Insert new classroom
        cursor = conn.execute('''
            INSERT INTO timetable_classrooms 
            (room_number, room_name, room_type, seating_capacity, facilities, 
             floor_number, building_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['room_number'],
            data['room_name'],
            data['room_type'],
            data['seating_capacity'],
            data.get('facilities', '{}'),
            data.get('floor_number'),
            data.get('building_name', '')
        ))
        
        classroom_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': classroom_id, 'message': 'Classroom created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Student Groups API
@timetable_bp.route('/student-groups', methods=['GET'])
@require_admin
def get_student_groups():
    """Get all student groups with coordinator details"""
    try:
        conn = get_db_connection()
        groups = conn.execute('''
            SELECT sg.*, 
                   t.first_name || ' ' || t.last_name as coordinator_name
            FROM timetable_student_groups sg
            LEFT JOIN timetable_teachers t ON sg.coordinator_teacher_id = t.id
            ORDER BY sg.group_code
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(group) for group in groups])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@timetable_bp.route('/student-groups', methods=['POST'])
@require_admin
def create_student_group():
    """Create a new student group"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['group_code', 'group_name', 'academic_year', 'semester', 'student_count']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        
        # Check if group code already exists
        existing = conn.execute(
            'SELECT id FROM timetable_student_groups WHERE group_code = ?',
            (data['group_code'],)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'error': 'Group code already exists'}), 400
        
        # Insert new student group
        cursor = conn.execute('''
            INSERT INTO timetable_student_groups 
            (group_code, group_name, academic_year, semester, student_count, 
             coordinator_teacher_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['group_code'],
            data['group_name'],
            data['academic_year'],
            data['semester'],
            data['student_count'],
            data.get('coordinator_teacher_id')
        ))
        
        group_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'id': group_id, 'message': 'Student group created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Statistics API
@timetable_bp.route('/stats', methods=['GET'])
@require_admin
def get_statistics():
    """Get statistics for the timetable management dashboard"""
    try:
        conn = get_db_connection()
        
        stats = {}
        
        # Count teachers
        result = conn.execute('SELECT COUNT(*) as count FROM timetable_teachers').fetchone()
        stats['teachers'] = result['count']
        
        # Count subjects
        result = conn.execute('SELECT COUNT(*) as count FROM timetable_subjects').fetchone()
        stats['subjects'] = result['count']
        
        # Count classrooms
        result = conn.execute('SELECT COUNT(*) as count FROM timetable_classrooms WHERE is_active = 1').fetchone()
        stats['classrooms'] = result['count']
        
        # Count student groups
        result = conn.execute('SELECT COUNT(*) as count FROM timetable_student_groups').fetchone()
        stats['student_groups'] = result['count']
        
        # Last generation info
        last_gen = conn.execute('''
            SELECT created_at FROM timetable_generations 
            WHERE generation_status = 'completed'
            ORDER BY created_at DESC LIMIT 1
        ''').fetchone()
        
        stats['last_generation'] = last_gen['created_at'] if last_gen else None
        
        conn.close()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Timetable Generation API
@timetable_bp.route('/generate', methods=['POST'])
@require_admin
def generate_timetable():
    """Generate automated timetable"""
    try:
        data = request.get_json()
        academic_year = data.get('academic_year', '2024-25')
        semester = data.get('semester', 1)
        method = data.get('method', 'auto')
        
        # Import the generation engine
        from timetable_generator import TimetableGenerator
        
        generator = TimetableGenerator()
        result = generator.generate_timetable(
            academic_year=academic_year,
            semester=semester,
            method=method,
            admin_user_id=session['user_id']
        )
        
        if result['success']:
            return jsonify({
                'message': 'Timetable generated successfully',
                'total_classes': result['total_classes'],
                'success_rate': result['success_rate'],
                'generation_id': result['generation_id']
            })
        else:
            return jsonify({
                'error': result['error'],
                'details': result.get('details', [])
            }), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Timetable View API
@timetable_bp.route('/view', methods=['GET'])
@require_admin
def get_timetable_view():
    """Get timetable data for viewing - Optimized version"""
    try:
        academic_year = request.args.get('academic_year', '2024-25')
        semester = request.args.get('semester', 1, type=int)
        group_id = request.args.get('group_id', type=int)
        teacher_id = request.args.get('teacher_id', type=int)
        classroom_id = request.args.get('classroom_id', type=int)
        
        conn = get_db_connection()
        
        # Optimized query with selective fields and better indexing
        query = '''
            SELECT te.id, te.session_type, te.created_at,
                   sg.group_code, sg.group_name,
                   s.subject_code, s.subject_name, s.subject_type,
                   t.first_name, t.last_name,
                   c.room_number, c.room_name, c.room_type,
                   ts.day_of_week, ts.start_time, ts.end_time, ts.slot_code, ts.slot_type
            FROM timetable_entries te
            INDEXED BY idx_timetable_entries_academic
            JOIN timetable_student_groups sg ON te.group_id = sg.id
            JOIN timetable_subjects s ON te.subject_id = s.id
            JOIN timetable_teachers t ON te.teacher_id = t.id
            JOIN timetable_classrooms c ON te.classroom_id = c.id
            JOIN time_slots ts ON te.time_slot_id = ts.id
            WHERE te.academic_year = ? AND te.semester = ? AND te.status = 'active'
        '''
        
        params = [academic_year, semester]
        
        # Add optimized filters with proper indexing
        if group_id:
            query = query.replace('INDEXED BY idx_timetable_entries_academic', 'INDEXED BY idx_timetable_entries_group')
            query += ' AND te.group_id = ?'
            params.append(group_id)
        elif teacher_id:
            query = query.replace('INDEXED BY idx_timetable_entries_academic', 'INDEXED BY idx_timetable_entries_teacher')
            query += ' AND te.teacher_id = ?'
            params.append(teacher_id)
        elif classroom_id:
            query = query.replace('INDEXED BY idx_timetable_entries_academic', 'INDEXED BY idx_timetable_entries_classroom')
            query += ' AND te.classroom_id = ?'
            params.append(classroom_id)
        
        # Optimized ordering using index
        query += ' ORDER BY ts.day_of_week, ts.start_time LIMIT 500'
        
        entries = conn.execute(query, params).fetchall()
        
        # Convert to optimized format
        result = []
        for entry in entries:
            result.append({
                'id': entry['id'],
                'session_type': entry['session_type'],
                'group_code': entry['group_code'],
                'group_name': entry['group_name'],
                'subject_code': entry['subject_code'],
                'subject_name': entry['subject_name'],
                'subject_type': entry['subject_type'],
                'teacher_name': f"{entry['first_name']} {entry['last_name']}",
                'room_number': entry['room_number'],
                'room_name': entry['room_name'],
                'room_type': entry['room_type'],
                'day_of_week': entry['day_of_week'],
                'start_time': entry['start_time'],
                'end_time': entry['end_time'],
                'slot_code': entry['slot_code'],
                'slot_type': entry['slot_type'],
                'created_at': entry['created_at']
            })
        
        conn.close()
        
        # Add cache headers for better performance
        response = jsonify(result)
        response.headers['Cache-Control'] = 'private, max-age=60'  # Cache for 1 minute
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Conflict Detection API
@timetable_bp.route('/conflicts', methods=['GET'])
@require_admin
def get_conflicts():
    """Get all conflicts in the current timetable"""
    try:
        academic_year = request.args.get('academic_year', '2024-25')
        semester = request.args.get('semester', 1, type=int)
        
        conn = get_db_connection()
        
        conflicts = conn.execute('''
            SELECT tc.*, te.id as entry_id,
                   sg.group_code, s.subject_name, 
                   t.first_name || ' ' || t.last_name as teacher_name,
                   c.room_number
            FROM timetable_conflicts tc
            JOIN timetable_entries te ON tc.entry_id = te.id
            JOIN timetable_student_groups sg ON te.group_id = sg.id
            JOIN timetable_subjects s ON te.subject_id = s.id
            JOIN timetable_teachers t ON te.teacher_id = t.id
            JOIN timetable_classrooms c ON te.classroom_id = c.id
            WHERE te.academic_year = ? AND te.semester = ? 
            AND tc.resolution_status = 'unresolved'
            ORDER BY tc.severity DESC, tc.detected_at DESC
        ''', (academic_year, semester)).fetchall()
        
        conn.close()
        return jsonify([dict(conflict) for conflict in conflicts])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500