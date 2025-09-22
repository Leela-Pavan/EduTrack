"""
Test the new click-to-verify system
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from verification_service import VerificationService

def test_click_verification():
    print("🎯 Testing New Click-to-Verify System")
    print("=" * 50)
    
    verification_service = VerificationService()
    
    # Test the new 3-option generation
    verification_data = verification_service.generate_verification_options()
    
    print("✨ Generated verification options:")
    print(f"   Option 1: {verification_data['options'][0]}")
    print(f"   Option 2: {verification_data['options'][1]}")
    print(f"   Option 3: {verification_data['options'][2]}")
    print()
    print(f"📧 Code sent to email: {verification_data['correct_code']}")
    print(f"🎯 Correct option index: {verification_data['correct_index']}")
    print()
    
    # Test email sending with correct code
    print("📨 Testing email sending:")
    email_result = verification_service.send_email_verification("test@example.com", verification_data['correct_code'])
    print(f"   Email sent: {'✅ Yes' if email_result else '❌ No'}")
    print()
    
    print("🎉 New verification system ready!")
    print()
    print("📋 How it works:")
    print("   1. User enters email")
    print("   2. Website shows 3 codes as buttons")
    print("   3. Only 1 code is sent to email")
    print("   4. User clicks the matching code")
    print("   5. ✅ Verified!")

if __name__ == "__main__":
    test_click_verification()