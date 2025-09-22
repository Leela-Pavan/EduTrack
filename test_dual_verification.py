"""
Test script to demonstrate dual verification (Email + Mobile)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verification_service import VerificationService
from config import Config

def test_dual_verification():
    print("🔒 Testing Dual Verification System (Email + Mobile)")
    print("=" * 60)
    
    # Create verification service
    verification_service = VerificationService()
    
    # Test data
    test_email = "student@example.com"
    test_mobile = "+1234567890"
    
    # Test sending both verification codes
    print("📧📱 Sending verification codes to BOTH email and mobile...")
    print()
    
    # Generate codes
    email_code = verification_service.generate_verification_code()
    mobile_code = verification_service.generate_verification_code()
    
    # Send email verification
    print("1️⃣ Sending EMAIL verification:")
    email_result = verification_service.send_email_verification(test_email, email_code)
    print(f"   Result: {'✅ Success' if email_result else '❌ Failed'}")
    print()
    
    # Send mobile verification  
    print("2️⃣ Sending MOBILE verification:")
    mobile_result = verification_service.send_sms_verification(test_mobile, mobile_code)
    print(f"   Result: {'✅ Success' if mobile_result else '❌ Failed'}")
    print()
    
    # Store both codes in database
    print("3️⃣ Storing verification codes in database...")
    store_result = verification_service.store_verification_codes(
        test_email, test_mobile, email_code, mobile_code
    )
    print(f"   Database storage: {'✅ Success' if store_result else '❌ Failed'}")
    print()
    
    # Test verification of both codes
    print("4️⃣ Testing verification of both codes:")
    
    # Verify email code
    email_verify = verification_service.verify_code(test_email, email_code, 'email')
    print(f"   Email verification: {'✅ ' + email_verify['message'] if email_verify['success'] else '❌ ' + email_verify['message']}")
    
    # Verify mobile code
    mobile_verify = verification_service.verify_code(test_mobile, mobile_code, 'mobile')
    print(f"   Mobile verification: {'✅ ' + mobile_verify['message'] if mobile_verify['success'] else '❌ ' + mobile_verify['message']}")
    print()
    
    print("🎉 Dual verification system test completed!")
    print()
    print("📋 Summary:")
    print(f"   • Email verification: {'Working ✅' if email_result and email_verify['success'] else 'Issues ❌'}")
    print(f"   • Mobile verification: {'Working ✅' if mobile_result and mobile_verify['success'] else 'Issues ❌'}")
    print(f"   • Database storage: {'Working ✅' if store_result else 'Issues ❌'}")

if __name__ == "__main__":
    test_dual_verification()