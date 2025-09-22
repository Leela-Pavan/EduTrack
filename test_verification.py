"""
Quick test script to verify the verification system is working
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verification_service import VerificationService
from config import Config

def test_verification():
    print("Testing EduTrack Verification System")
    print("=" * 40)
    
    # Test configuration loading
    print(f"Development Mode: {os.getenv('DEVELOPMENT_MODE', 'False')}")
    print(f"Mail Username: {Config.MAIL_USERNAME or 'Not configured'}")
    print(f"Twilio SID: {Config.TWILIO_ACCOUNT_SID or 'Not configured'}")
    print()
    
    # Create verification service instance
    verification_service = VerificationService()
    
    # Test email verification
    print("Testing Email Verification:")
    email_code = verification_service.generate_verification_code()
    email_result = verification_service.send_email_verification("test@example.com", email_code)
    print(f"Email Result: {email_result}")
    print()
    
    # Test SMS verification
    print("Testing SMS Verification:")
    sms_code = verification_service.generate_verification_code()
    sms_result = verification_service.send_sms_verification("+1234567890", sms_code)
    print(f"SMS Result: {sms_result}")
    print()
    
    print("✅ Verification system test completed!")

if __name__ == "__main__":
    test_verification()