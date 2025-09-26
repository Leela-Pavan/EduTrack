#!/usr/bin/env python3
"""
Test script for student profile functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_student_profile():
    # Create session
    session = requests.Session()
    
    print("Testing Student Profile Functionality...")
    
    # First, let's try to login as a student
    # Check if we have any students in the database
    try:
        # Try to register a new student first
        register_data = {
            'username': 'test_student_profile',
            'email': 'test.student@example.com',
            'password': 'password123',
            'role': 'student',
            'first_name': 'Test',
            'last_name': 'Student',
            'student_id': 'TS001',
            'department': 'Computer Science',
            'section': 'A',
            'year': '2024'
        }
        
        response = session.post(f"{BASE_URL}/register", data=register_data)
        print(f"Registration status: {response.status_code}")
        
        # Now login
        login_data = {
            'username': 'test_student_profile',
            'password': 'password123'
        }
        
        response = session.post(f"{BASE_URL}/login", data=login_data)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            # Test profile update
            profile_update_data = {
                'first_name': 'Updated Test',
                'last_name': 'Updated Student',
                'email': 'updated.test.student@example.com',
                'department': 'Information Technology',
                'section': 'B',
                'year': '2025',
                'date_of_birth': '2000-01-15',
                'mobile': '+1234567890'
            }
            
            headers = {'Content-Type': 'application/json'}
            response = session.post(f"{BASE_URL}/api/update_student_profile", 
                                  json=profile_update_data, headers=headers)
            print(f"Profile update status: {response.status_code}")
            print(f"Profile update response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Student profile update successful!")
                result = response.json()
                if result.get('success'):
                    print("✅ Profile update completed successfully!")
                else:
                    print(f"❌ Profile update failed: {result.get('error')}")
            else:
                print(f"❌ Profile update failed with status {response.status_code}")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error testing student profile: {e}")

if __name__ == "__main__":
    test_student_profile()