import sqlite3import sqlite3import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.security import check_password_hash, generate_password_hashfrom werkzeug.security import generate_password_hash

conn = sqlite3.connect('school_system.db')

cursor = conn.cursor()



test_username = "testuser123"# Let's create a test user with a known password to verify the login process worksdef create_test_user():

test_password = "testpass123"

conn = sqlite3.connect('school_system.db')    conn = sqlite3.connect('school_system.db')

cursor.execute('DELETE FROM users WHERE username = ?', (test_username,))

cursor = conn.cursor()    cursor = conn.cursor()

password_hash = generate_password_hash(test_password)

cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',

               (test_username, password_hash, 'student', 'test@test.com'))

# Create a test user    # Check if student already exists

user_id = cursor.lastrowid

print(f"Created test user: {test_username} with password: {test_password}")test_username = "testuser123"    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('student1',))



cursor.execute('SELECT id, password_hash, role FROM users WHERE username = ?', (test_username,))test_password = "testpass123"    if cursor.fetchone()[0] > 0:

user = cursor.fetchone()

        print('Test student already exists')

if user and check_password_hash(user[1], test_password):

    print("✓ Test user login verification successful")# Delete test user if exists        print('Username: student1')

else:

    print("✗ Test user login verification failed")cursor.execute('DELETE FROM users WHERE username = ?', (test_username,))        print('Password: password123')



conn.commit()        conn.close()

conn.close()

# Create new test user        return

print(f"\nTest login credentials:")

print(f"Username: {test_username}")password_hash = generate_password_hash(test_password)

print(f"Password: {test_password}")
cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',    # Create a test student user

               (test_username, password_hash, 'student', 'test@test.com'))    password_hash = generate_password_hash('password123')

    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)', 

user_id = cursor.lastrowid                   ('student1', password_hash, 'student', 'student1@test.com'))

print(f"Created test user: {test_username} with password: {test_password}")    user_id = cursor.lastrowid



# Verify the user works    # Create student profile

cursor.execute('SELECT id, password_hash, role FROM users WHERE username = ?', (test_username,))    cursor.execute('INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',

user = cursor.fetchone()                   (user_id, 'STU001', 'John', 'Doe', '10', 'A', 'Science', 'Math', 'Engineer'))



if user and check_password_hash(user[1], test_password):    conn.commit()

    print("✓ Test user login verification successful")    conn.close()

else:    print('Test student created successfully')

    print("✗ Test user login verification failed")    print('Username: student1')

    print('Password: password123')

conn.commit()

conn.close()if __name__ == '__main__':

    create_test_user()
print(f"\nYou can now test login with:")
print(f"Username: {test_username}")
print(f"Password: {test_password}")