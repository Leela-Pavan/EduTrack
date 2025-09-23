import requests

# Test student registration
student_data = {
    'username': 'testuser123',
    'email': 'test@example.com',
    'password': 'password123',
    'role': 'student',
    'student_id': 'ST001',
    'first_name': 'Test',
    'last_name': 'User',
    'department': 'CSD',
    'section': 'A',
    'year': '1',
    'mobile_number': '9876543210'
}

try:
    response = requests.post('http://127.0.0.1:5000/register', data=student_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")  # First 500 chars
    print("Registration test completed")
except Exception as e:
    print(f"Error: {e}")