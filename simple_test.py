import requests

data = {
    'username': 'test123',
    'email': 'test@test.com', 
    'password': 'password123',
    'role': 'student',
    'student_id': 'ST001',
    'first_name': 'Test',
    'last_name': 'User',
    'department': 'CSD',
    'section': 'A',
    'year': '1'
}

try:
    response = requests.post('http://127.0.0.1:5000/register', data=data)
    print(f"Status: {response.status_code}")
    if 'Registration successful' in response.text:
        print("SUCCESS: Registration completed!")
    elif 'error' in response.text.lower():
        print("ERROR found in response")
    print(f"Response length: {len(response.text)}")
except Exception as e:
    print(f"Error: {e}")