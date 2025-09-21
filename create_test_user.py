import sqlite3
from werkzeug.security import generate_password_hash

def create_test_user():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()

    # Check if student already exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('student1',))
    if cursor.fetchone()[0] > 0:
        print('Test student already exists')
        print('Username: student1')
        print('Password: password123')
        conn.close()
        return

    # Create a test student user
    password_hash = generate_password_hash('password123')
    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)', 
                   ('student1', password_hash, 'student', 'student1@test.com'))
    user_id = cursor.lastrowid

    # Create student profile
    cursor.execute('INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, 'STU001', 'John', 'Doe', '10', 'A', 'Science', 'Math', 'Engineer'))

    conn.commit()
    conn.close()
    print('Test student created successfully')
    print('Username: student1')
    print('Password: password123')

if __name__ == '__main__':
    create_test_user()