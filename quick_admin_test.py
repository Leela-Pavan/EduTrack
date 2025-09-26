import requests

session = requests.Session()
response = session.post('http://127.0.0.1:5000/login', data={'username': 'ADMIN', 'password': 'ADMIN'})
print(f'Login: {response.status_code}, URL: {response.url}')

response = session.get('http://127.0.0.1:5000/admin/dashboard')
print(f'Dashboard: {response.status_code}')
print(f'Contains student data: {"Total Students" in response.text}')
print(f'Contains teacher data: {"Total Teachers" in response.text}')