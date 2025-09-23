import requests

# Teacher registration data as specified
teacher_data = {
    'username': 'Raju',
    'email': 'raju@gmail.com',
    'password': '2580',
    'role': 'teacher',
    'teacher_id': '101',
    'first_name': 'Raju',
    'last_name': '',  # Using empty string since only one name was provided
    'subject': 'DLCO',
    'designation': 'Asst Prof',
    'mobile_number': '9885618712'
}

print("Testing Teacher Registration:")
print("=" * 40)
print(f"Username: {teacher_data['username']}")
print(f"Email: {teacher_data['email']}")
print(f"Role: {teacher_data['role']}")
print(f"Teacher ID: {teacher_data['teacher_id']}")
print(f"Subject: {teacher_data['subject']}")
print(f"Designation: {teacher_data['designation']}")
print(f"Mobile: {teacher_data['mobile_number']}")
print("=" * 40)

try:
    # Send POST request to register endpoint
    response = requests.post('http://127.0.0.1:5000/register', data=teacher_data)
    
    print(f"Status Code: {response.status_code}")
    
    # Check if registration was successful
    if response.status_code == 200:
        if 'Registration successful' in response.text:
            print("✅ SUCCESS: Teacher registration completed successfully!")
            print("User should be redirected to login page.")
        elif 'already exists' in response.text:
            print("⚠️  WARNING: Username or email already exists in the database.")
        elif 'error' in response.text.lower() or 'failed' in response.text.lower():
            print("❌ ERROR: Registration failed.")
            # Try to extract error message
            if 'Registration failed:' in response.text:
                start = response.text.find('Registration failed:')
                end = response.text.find('<', start)
                if end == -1:
                    end = start + 100
                error_msg = response.text[start:end]
                print(f"Error details: {error_msg}")
        else:
            print("📄 Response received but status unclear.")
            print("Checking response content...")
            
    elif response.status_code == 302:
        print("✅ SUCCESS: Registration completed! (Redirect response)")
        print("User should be redirected to login page.")
    else:
        print(f"❌ ERROR: Unexpected status code {response.status_code}")
        
    print(f"Response length: {len(response.text)} characters")
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Could not connect to the Flask application.")
    print("Make sure the Flask app is running on http://127.0.0.1:5000")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

print("=" * 40)
print("Registration test completed.")