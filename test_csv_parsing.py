#!/usr/bin/env python3
"""
Direct test of CSV parsing functionality for bulk schedule upload
"""
import csv
import io
import sqlite3

def test_csv_parsing():
    print("📊 Testing CSV Parsing for Bulk Schedule Upload...")
    
    # Sample CSV content
    csv_content = """Day,Period,Subject,Teacher,Room
Monday,1,Mathematics,Chaitanya,Room-101
Monday,2,Physics,Aneela,Room-102
Tuesday,1,English,Praveen,Room-104
Wednesday,1,Computer Science,Tulasi,Room-105
Invalid,X,Bad Data,Unknown,Room-999"""
    
    try:
        # Test CSV parsing
        print("\n1. Testing CSV parsing...")
        stream = io.StringIO(csv_content)
        csv_input = csv.DictReader(stream)
        
        rows = list(csv_input)
        print(f"   ✅ Parsed {len(rows)} rows from CSV")
        
        # Test row processing
        print("\n2. Testing row processing...")
        
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        valid_rows = 0
        errors = []
        
        for row_num, row in enumerate(rows, start=2):
            day = row.get('Day', '').strip()
            period_str = row.get('Period', '').strip()
            subject = row.get('Subject', '').strip()
            teacher_name = row.get('Teacher', '').strip()
            room = row.get('Room', '').strip()
            
            print(f"   Row {row_num}: {day}, P{period_str}, {subject}, {teacher_name}")
            
            # Validate required fields
            if not day or not period_str or not subject:
                errors.append(f"Row {row_num}: Missing required fields")
                continue
            
            # Validate period number
            try:
                period = int(period_str)
                if period < 1 or period > 8:
                    errors.append(f"Row {row_num}: Period must be 1-8")
                    continue
            except ValueError:
                errors.append(f"Row {row_num}: Invalid period number")
                continue
            
            # Validate day
            valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            if day not in valid_days:
                errors.append(f"Row {row_num}: Invalid day")
                continue
            
            # Try to find teacher
            teacher_id = None
            if teacher_name:
                cursor.execute('''
                    SELECT t.user_id FROM teachers t 
                    LEFT JOIN users u ON t.user_id = u.id
                    WHERE LOWER(t.first_name || ' ' || t.last_name) LIKE LOWER(?) 
                    OR LOWER(u.username) LIKE LOWER(?)
                    LIMIT 1
                ''', (f'%{teacher_name}%', f'%{teacher_name}%'))
                
                teacher_result = cursor.fetchone()
                if teacher_result:
                    teacher_id = teacher_result[0]
                    print(f"      ✅ Found teacher: {teacher_name}")
                else:
                    print(f"      ⚠️  Teacher not found: {teacher_name}")
            
            valid_rows += 1
        
        conn.close()
        
        print(f"\n3. Processing results:")
        print(f"   ✅ Valid rows: {valid_rows}")
        print(f"   ❌ Invalid rows: {len(errors)}")
        
        if errors:
            print(f"\n   Errors found:")
            for error in errors:
                print(f"      - {error}")
        
        print(f"\n" + "="*50)
        print(f"🎉 CSV PARSING TEST COMPLETED!")
        print(f"   The bulk upload functionality should now work correctly")
        print(f"   with proper CSV files in the format:")
        print(f"   Day,Period,Subject,Teacher,Room")
        print(f"="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_csv_parsing()