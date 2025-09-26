import requests
import json

session = requests.Session()

# Login as admin
response = session.post('http://127.0.0.1:5000/login', data={'username': 'ADMIN', 'password': 'ADMIN'})
print(f'Admin Login: {response.status_code}')

if response.status_code == 200:
    # Test API endpoints
    endpoints = [
        '/api/students',
        '/api/teachers',
        '/api/attendance_stats'
    ]
    
    for endpoint in endpoints:
        response = session.get(f'http://127.0.0.1:5000{endpoint}')
        print(f'\n{endpoint}: {response.status_code}')
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f'  Data type: List with {len(data)} items')
                    if data:
                        print(f'  Sample item keys: {list(data[0].keys()) if data else "No data"}')
                elif isinstance(data, dict):
                    print(f'  Data type: Dict with keys: {list(data.keys())}')
                else:
                    print(f'  Data type: {type(data)}')
            except json.JSONDecodeError:
                print(f'  Content (first 200 chars): {response.text[:200]}')
        else:
            print(f'  Error: {response.status_code}')
            
    # Test dashboard page content
    response = session.get('http://127.0.0.1:5000/admin/dashboard')
    if response.status_code == 200:
        content = response.text
        print(f'\nDashboard Content Analysis:')
        print(f'  Contains "Total Students": {"Total Students" in content}')
        print(f'  Contains "Total Teachers": {"Total Teachers" in content}')
        print(f'  Contains attendance data: {"attendance_stats" in content or "Present" in content}')
        print(f'  Page length: {len(content)} characters')
else:
    print('Admin login failed!')