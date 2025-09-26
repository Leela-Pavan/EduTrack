import sqlite3

conn = sqlite3.connect('school_system.db')
cursor = conn.cursor()

# Check sample timetable row
cursor.execute("SELECT * FROM timetable WHERE class_name = 'CSIT' AND section = 'A' AND day_of_week = 'Tuesday' LIMIT 1")
row = cursor.fetchone()
print('Sample CSIT-A Tuesday row:', row)
print('Row length:', len(row) if row else 0)

# Get column details
cursor.execute('PRAGMA table_info(timetable)')
columns = cursor.fetchall()
print('\nColumn mapping:')
for i, col in enumerate(columns):
    print(f'Index {i}: {col[1]} ({col[2]})')

conn.close()