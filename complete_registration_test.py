import requests
import time

def test_teacher_registration():
    print("Testing Teacher Registration with Provided Data")
    print("=" * 55)
    
    # Teacher registration data exactly as specified
    teacher_data = {
        'username': 'Raju',
        'email': 'raju@gmail.com',
        'password': '2580',
        'role': 'teacher',
        'teacher_id': '101',
        'first_name': 'Raju',
        'last_name': '',  # Empty since only one name provided
        'subject': 'DLCO',
        'designation': 'Asst Prof',
        'mobile_number': '9885618712'
    }
    
    print("Registration Data:")
    for key, value in teacher_data.items():
        print(f"  {key}: {value}")
    print("-" * 55)
    
    try:
        # Test connection first
        print("1. Testing connection to Flask app...")
        response = requests.get('http://127.0.0.1:5000/register', timeout=10)
        if response.status_code == 200:
            print("   ✅ Connection successful")
        else:
            print(f"   ❌ Connection failed: {response.status_code}")
            return
            
        # Attempt registration
        print("2. Submitting registration data...")
        response = requests.post('http://127.0.0.1:5000/register', data=teacher_data, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        # Analyze response
        if response.status_code == 200:
            # Check for success or error messages in the response
            response_text = response.text.lower()
            
            if 'registration successful' in response_text or 'login' in response_text:
                print("   ✅ Registration appears successful!")
            elif 'already exists' in response_text:
                print("   ⚠️  User already exists in database")
            elif 'error' in response_text or 'failed' in response_text:
                print("   ❌ Registration failed")
                # Try to find specific error
                if 'missing required field' in response_text:
                    print("   → Missing required field error")
                elif 'registration failed' in response_text:
                    print("   → General registration failure")
            else:
                print("   📄 Response received but unclear status")
                
        elif response.status_code == 302:
            print("   ✅ Registration successful (redirect response)")
            # Check redirect location
            if 'location' in response.headers:
                location = response.headers['location']
                print(f"   → Redirected to: {location}")
                if 'login' in location:
                    print("   → Successfully redirected to login page")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            
        print(f"   Response length: {len(response.text)} characters")
        
        # Wait a moment for database writes to complete
        print("3. Waiting for database update...")
        time.sleep(2)
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ ERROR: Cannot connect to Flask application")
        print("   → Make sure Flask app is running on http://127.0.0.1:5000")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ ERROR: Request timed out")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_teacher_registration()
    
    if success:
        print("\n" + "=" * 55)
        print("Now checking database for registration...")
        print("=" * 55)
        
        # Import and run the database check
        import subprocess
        import sys
        
        try:
            result = subprocess.run([sys.executable, 'check_registration.py'], 
                                  capture_output=True, text=True, timeout=10)
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        except Exception as e:
            print(f"Error running database check: {e}")
    
    print("\nRegistration test completed!")