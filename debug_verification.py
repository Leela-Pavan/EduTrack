"""
Debug verification issue
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Debugging Verification Configuration")
print("=" * 40)

print(f"DEVELOPMENT_MODE value: '{os.getenv('DEVELOPMENT_MODE', 'Not Set')}'")
print(f"DEVELOPMENT_MODE check: {os.getenv('DEVELOPMENT_MODE', 'False').lower() == 'true'}")

from config import Config
print(f"MAIL_USERNAME: '{Config.MAIL_USERNAME or 'Not Set'}'")
print(f"Config check: {not Config.MAIL_USERNAME}")

# Test the condition
development_mode = os.getenv('DEVELOPMENT_MODE', 'False').lower() == 'true'
print(f"Should be in dev mode: {development_mode or not Config.MAIL_USERNAME}")

if development_mode or not Config.MAIL_USERNAME:
    print("✅ Should show codes in console")
else:
    print("❌ Should try to send real emails")