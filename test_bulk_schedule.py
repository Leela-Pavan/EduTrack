#!/usr/bin/env python3
"""
Test bulk schedule upload functionality
"""
import requests
import os

def test_bulk_schedule_upload():
    print("📊 Testing Bulk Schedule Upload...")
    
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    try:
        # Test login first
        print("\n1. Testing admin login...")
        login_data = {
            'email': 'admin@school.com',
            'password': 'admin123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data, timeout=10)
        
        if login_response.status_code == 200:
            print("✅ Admin logged in successfully")
        else:
            print(f"❌ Login failed - Status: {login_response.status_code}")
            return
        
        # Test CSV file upload
        print("\n2. Testing CSV bulk upload...")
        
        csv_file_path = "sample_schedule.csv"
        if not os.path.exists(csv_file_path):
            print(f"❌ Sample CSV file not found: {csv_file_path}")
            return
        
        # Prepare form data
        with open(csv_file_path, 'rb') as f:
            files = {'file': ('sample_schedule.csv', f, 'text/csv')}
            data = {
                'class_name': 'CSIT',
                'section': 'A', 
                'replace_existing': 'true'
            }
            
            print(f"   Uploading CSV for class: CSIT-A")
            print(f"   Replace existing: True")
            
            upload_response = session.post(
                f"{base_url}/api/bulk-schedule",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"   Response Status: {upload_response.status_code}")
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            print(f"   Response: {result}")
            
            if result.get('success'):
                print(f"   ✅ Bulk upload successful!")
                print(f"   📊 Imported schedules: {result.get('imported', 0)}")
                
                if 'warnings' in result:
                    print(f"   ⚠️  Warnings: {len(result['warnings'])}")
                    for warning in result['warnings'][:3]:  # Show first 3 warnings
                        print(f"      - {warning}")
            else:
                print(f"   ❌ Upload failed: {result.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ HTTP Error: {upload_response.status_code}")
            print(f"   Response: {upload_response.text[:200]}")
        
        # Test schedule retrieval to verify upload
        print(f"\n3. Verifying uploaded schedules...")
        schedules_response = session.get(f"{base_url}/api/schedules", timeout=10)
        
        if schedules_response.status_code == 200:
            schedules = schedules_response.json()
            csit_a_schedules = [s for s in schedules if s.get('class_name') == 'CSIT' and s.get('section') == 'A']
            print(f"   ✅ Found {len(csit_a_schedules)} schedules for CSIT-A")
            
            if csit_a_schedules:
                print(f"   Sample schedules:")
                for schedule in csit_a_schedules[:3]:
                    print(f"      {schedule.get('day_of_week')} P{schedule.get('period_number')}: {schedule.get('subject')}")
        
        print(f"\n" + "="*50)
        print(f"🎉 BULK SCHEDULE UPLOAD TEST COMPLETED!")
        print(f"="*50)
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_bulk_schedule_upload()