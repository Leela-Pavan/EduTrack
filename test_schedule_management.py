#!/usr/bin/env python3
"""
Test the schedule management functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_schedule_management():
    print("🗓️ Testing Schedule Management System...")
    
    session = requests.Session()
    
    # Login as admin
    login_response = session.post(f"{BASE_URL}/login", data={
        'username': 'ADMIN',
        'password': 'ADMIN'
    })
    
    if login_response.status_code != 200:
        print("❌ Admin login failed")
        return False
    
    print("✅ Admin logged in successfully")
    
    # Test 1: Access manage schedule page
    print("\n1. Testing schedule management page access...")
    response = session.get(f"{BASE_URL}/admin/manage-schedule")
    if response.status_code == 200:
        print("✅ Schedule management page accessible")
        if "Schedule Management" in response.text:
            print("✅ Page content loaded correctly")
        else:
            print("❌ Page content missing")
    else:
        print(f"❌ Schedule management page failed: {response.status_code}")
        return False
    
    # Test 2: Get schedules API
    print("\n2. Testing schedules API...")
    response = session.get(f"{BASE_URL}/api/schedules")
    if response.status_code == 200:
        schedules = response.json()
        print(f"✅ Schedules API working - found {len(schedules)} existing schedules")
    else:
        print(f"❌ Schedules API failed: {response.status_code}")
        return False
    
    # Test 3: Add a new schedule
    print("\n3. Testing add schedule...")
    new_schedule = {
        "class_name": "CSIT",
        "section": "A",
        "day_of_week": "Monday",
        "period_number": 1,
        "subject": "Mathematics",
        "teacher_id": 8,  # Assuming teacher ID 8 exists
        "start_time": "09:00",
        "end_time": "09:50"
    }
    
    response = session.post(f"{BASE_URL}/api/schedule", 
                           headers={'Content-Type': 'application/json'},
                           json=new_schedule)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✅ Schedule added successfully")
        else:
            print(f"❌ Schedule add failed: {result.get('error')}")
    else:
        print(f"❌ Add schedule API failed: {response.status_code}")
    
    # Test 4: Test bulk schedule
    print("\n4. Testing bulk schedule...")
    bulk_data = {
        "classes": ["CSIT-A", "CSIT-B"],
        "days": ["Tuesday", "Wednesday"],
        "periods": [2, 3],
        "subject": "Physics",
        "teacher_id": 8
    }
    
    response = session.post(f"{BASE_URL}/api/bulk-schedule",
                           headers={'Content-Type': 'application/json'},
                           json=bulk_data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"✅ Bulk schedule created - {result.get('created', 0)} entries")
        else:
            print(f"❌ Bulk schedule failed: {result.get('error')}")
    else:
        print(f"❌ Bulk schedule API failed: {response.status_code}")
    
    # Test 5: Get teacher schedules
    print("\n5. Testing teacher schedules API...")
    response = session.get(f"{BASE_URL}/api/teacher-schedules")
    if response.status_code == 200:
        teacher_schedules = response.json()
        print(f"✅ Teacher schedules API working - {len(teacher_schedules)} teachers have schedules")
        for teacher, schedules in teacher_schedules.items():
            print(f"   - {teacher}: {len(schedules)} periods")
    else:
        print(f"❌ Teacher schedules API failed: {response.status_code}")
    
    # Test 6: Check conflicts
    print("\n6. Testing schedule conflicts check...")
    response = session.get(f"{BASE_URL}/api/schedule-conflicts")
    if response.status_code == 200:
        conflicts = response.json()
        conflict_count = len(conflicts.get('conflicts', []))
        print(f"✅ Conflict check working - found {conflict_count} conflicts")
        if conflict_count > 0:
            for conflict in conflicts['conflicts']:
                print(f"   ⚠️  {conflict['description']}")
    else:
        print(f"❌ Schedule conflicts API failed: {response.status_code}")
    
    # Test 7: Get updated schedules count
    print("\n7. Verifying schedule creation...")
    response = session.get(f"{BASE_URL}/api/schedules")
    if response.status_code == 200:
        final_schedules = response.json()
        print(f"✅ Final schedule count: {len(final_schedules)} schedules")
        
        # Show sample schedules
        for schedule in final_schedules[:3]:
            print(f"   - {schedule['class_name']}-{schedule['section']} {schedule['day_of_week']} P{schedule['period_number']}: {schedule['subject']} ({schedule.get('teacher_name', 'No teacher')})")
    else:
        print(f"❌ Final schedules check failed: {response.status_code}")
    
    print("\n" + "="*50)
    print("🎉 SCHEDULE MANAGEMENT SYSTEM TEST COMPLETED!")
    print("="*50)
    
    return True

if __name__ == "__main__":
    test_schedule_management()