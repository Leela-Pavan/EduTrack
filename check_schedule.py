import sqlite3

conn = sqlite3.connect('school_system.db')
cursor = conn.cursor()

# Check CSIT-A schedule
cursor.execute("""SELECT day_of_week, period_number, subject, start_time, end_time 
                  FROM timetable 
                  WHERE class_name = 'CSIT' AND section = 'A' 
                  ORDER BY day_of_week, period_number""")

rows = cursor.fetchall()
print('CSIT-A Schedule:')
for row in rows:
    print(f'{row[0]} Period {row[1]}: {row[2]} ({row[3]}-{row[4]})')

# Check what day today is
from datetime import datetime
today = datetime.now().strftime('%A')
print(f'\nToday is: {today}')

# Check today's schedule for CSIT-A
cursor.execute("""SELECT period_number, subject, start_time, end_time 
                  FROM timetable 
                  WHERE class_name = 'CSIT' AND section = 'A' AND day_of_week = ?
                  ORDER BY period_number""", (today,))

today_schedule = cursor.fetchall()
print(f'\nToday\'s CSIT-A Schedule ({today}):')
for row in today_schedule:
    print(f'Period {row[0]}: {row[1]} ({row[2]}-{row[3]})')

conn.close()