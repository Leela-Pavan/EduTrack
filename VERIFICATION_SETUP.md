# Email and Mobile Verification Setup Guide

## Overview
The EduTrack system now includes email and mobile number verification during student registration. This ensures that students provide valid contact information.

## Features Implemented
✅ Email verification with 6-digit codes
✅ Mobile SMS verification with 6-digit codes  
✅ Real-time verification status in registration form
✅ Secure code storage with expiration (10 minutes)
✅ Rate limiting (max 3 attempts per verification)
✅ Visual feedback and status indicators

## Setup Instructions

### 1. Email Service Setup (Gmail)
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Create password for "Mail" application
3. Update environment variables:
   ```
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_16_character_app_password
   ```

### 2. SMS Service Setup (Twilio)
1. Sign up for Twilio account at https://www.twilio.com
2. Get a phone number from Twilio Console
3. Copy credentials from Twilio Console:
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

### 3. Environment Configuration
1. Copy `.env.example` to `.env`
2. Update with your actual credentials
3. Install python-dotenv if not already installed:
   ```bash
   pip install python-dotenv
   ```

### 4. Database Migration
The database has been automatically updated with verification fields:
- `users.mobile_number` - stores mobile number
- `users.email_verified` - tracks email verification status
- `users.mobile_verified` - tracks mobile verification status
- `verification_codes` table - stores temporary verification codes

## How It Works

### Registration Flow:
1. Student enters email and mobile number
2. Clicks "Send Code" buttons to receive verification codes
3. Enters received codes in verification fields
4. Clicks "Verify" to validate codes
5. Form submission only allowed after both verifications (if both fields filled)

### Security Features:
- Codes expire after 10 minutes
- Maximum 3 verification attempts per session
- Codes are 6 digits long (numeric only)
- Secure storage with timestamps
- Rate limiting on code generation

## Development Mode
If email/SMS services are not configured, the system will:
- Print verification codes to console for testing
- Still validate the verification flow
- Allow development without external services

## Production Considerations
1. Use environment variables for all credentials
2. Enable HTTPS for secure transmission
3. Consider SMS costs and implement usage limits
4. Set up monitoring for failed verification attempts
5. Implement backup verification methods

## Testing
1. Start the application: `python app.py`
2. Navigate to registration page
3. Select "Student" role to see verification fields
4. Test with valid email and mobile number
5. Check console output for verification codes in development mode

## Troubleshooting
- **Email not sending**: Check Gmail app password and 2FA setup
- **SMS not sending**: Verify Twilio credentials and phone number format
- **Codes not working**: Check system time and code expiration
- **Database errors**: Run migration script again if needed

## Files Modified/Created:
- `templates/register.html` - Added verification UI
- `app.py` - Added verification routes and updated registration
- `verification_service.py` - Core verification logic
- `config.py` - Added verification configuration
- `migrate_verification.py` - Database migration script
- `requirements.txt` - Added Twilio dependency