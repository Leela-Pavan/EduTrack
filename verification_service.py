"""
Verification Service for Email and SMS
Handles sending and validating verification codes
"""
import random
import string
import sqlite3
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from twilio.rest import Client
import os
from config import Config

class VerificationService:
    def __init__(self, app=None):
        self.app = app
        self.mail = None
        self.twilio_client = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        self.mail = Mail(app)
        
        # Initialize Twilio client if credentials are provided
        if Config.TWILIO_ACCOUNT_SID and Config.TWILIO_AUTH_TOKEN:
            self.twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    
    def generate_verification_options(self):
        """Generate 3 verification codes, return all 3 and mark which one is correct"""
        codes = []
        for _ in range(3):
            code = ''.join(random.choices(string.digits, k=6))
            codes.append(code)
        
        # Randomly select which code to send to email (0, 1, or 2)
        correct_index = random.choice([0, 1, 2])
        correct_code = codes[correct_index]
        
        return {
            'options': codes,
            'correct_code': correct_code,
            'correct_index': correct_index
        }
    
    def generate_verification_code(self, length=6):
        """Generate a random verification code"""
        return ''.join(random.choices(string.digits, k=length))
    
    def send_email_verification(self, email, code):
        """Send verification code via email"""
        try:
            # Check if we're in development mode or email not configured
            development_mode = os.getenv('DEVELOPMENT_MODE', 'True').lower() == 'true'
            email_configured = Config.MAIL_USERNAME and Config.MAIL_USERNAME != 'your_email@gmail.com'
            
            if development_mode or not email_configured:
                print(f"\n📧 EMAIL VERIFICATION CODE for {email}: {code}")
                print(f"⏰ Code expires in {Config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes")
                print("=" * 50)
                return True
            
            msg = Message(
                'EduTrack - Email Verification Code',
                sender=Config.MAIL_DEFAULT_SENDER,
                recipients=[email]
            )
            msg.body = f"""
Hello,

Your EduTrack email verification code is: {code}

This code will expire in {Config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes.

If you didn't request this verification, please ignore this email.

Best regards,
EduTrack Team
            """
            msg.html = f"""
<html>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #007bff;">EduTrack - Email Verification</h2>
        <p>Hello,</p>
        <p>Your email verification code is:</p>
        <div style="background-color: #f8f9fa; border: 2px dashed #007bff; padding: 20px; text-align: center; margin: 20px 0;">
            <h1 style="color: #007bff; margin: 0; letter-spacing: 5px;">{code}</h1>
        </div>
        <p>This code will expire in <strong>{Config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes</strong>.</p>
        <p>If you didn't request this verification, please ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #dee2e6; margin: 20px 0;">
        <p style="color: #6c757d; font-size: 12px;">Best regards,<br>EduTrack Team</p>
    </div>
</body>
</html>
            """
            
            if self.mail:
                self.mail.send(msg)
                print(f"✅ Email verification code sent to {email}")
                return True
            else:
                print(f"❌ Email service not configured properly")
                return False
        except Exception as e:
            print(f"❌ Failed to send email to {email}: {str(e)}")
            return False
    
    def send_sms_verification(self, mobile_number, code):
        """Send verification code via SMS"""
        try:
            # Check if we're in development mode or SMS not configured
            development_mode = os.getenv('DEVELOPMENT_MODE', 'True').lower() == 'true'
            sms_configured = Config.TWILIO_ACCOUNT_SID and Config.TWILIO_ACCOUNT_SID != 'your_account_sid_here'
            
            if development_mode or not sms_configured:
                print(f"\n📱 SMS VERIFICATION CODE for {mobile_number}: {code}")
                print(f"⏰ Code expires in {Config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes")
                print("=" * 50)
                return True
            
            if self.twilio_client and Config.TWILIO_PHONE_NUMBER:
                message = self.twilio_client.messages.create(
                    body=f"Your EduTrack verification code is: {code}. Valid for {Config.VERIFICATION_CODE_EXPIRY_MINUTES} minutes.",
                    from_=Config.TWILIO_PHONE_NUMBER,
                    to=mobile_number
                )
                print(f"✅ SMS verification code sent to {mobile_number}")
                return True
            else:
                print(f"❌ SMS service not configured properly")
                return False
        except Exception as e:
            print(f"❌ Failed to send SMS to {mobile_number}: {str(e)}")
            return False
    
    def store_verification_codes(self, email, mobile_number, email_code, mobile_code, user_id=None):
        """Store verification codes in database"""
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        expiry_time = datetime.now() + timedelta(minutes=Config.VERIFICATION_CODE_EXPIRY_MINUTES)
        
        try:
            # Check if record exists for this email/mobile
            cursor.execute('''
                SELECT id FROM verification_codes 
                WHERE email = ? OR mobile_number = ?
            ''', (email, mobile_number))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE verification_codes 
                    SET email_code = ?, mobile_code = ?, 
                        email_code_expiry = ?, mobile_code_expiry = ?,
                        email_attempts = 0, mobile_attempts = 0,
                        user_id = ?
                    WHERE email = ? OR mobile_number = ?
                ''', (email_code, mobile_code, expiry_time, expiry_time, user_id, email, mobile_number))
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO verification_codes 
                    (user_id, email, mobile_number, email_code, mobile_code, 
                     email_code_expiry, mobile_code_expiry)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, email, mobile_number, email_code, mobile_code, expiry_time, expiry_time))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Failed to store verification codes: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def verify_code(self, identifier, code, verification_type='email'):
        """Verify a code (email or mobile)"""
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        try:
            if verification_type == 'email':
                cursor.execute('''
                    SELECT id, email_code, email_code_expiry, email_attempts 
                    FROM verification_codes 
                    WHERE email = ?
                ''', (identifier,))
            else:  # mobile
                cursor.execute('''
                    SELECT id, mobile_code, mobile_code_expiry, mobile_attempts 
                    FROM verification_codes 
                    WHERE mobile_number = ?
                ''', (identifier,))
            
            result = cursor.fetchone()
            if not result:
                return {'success': False, 'message': 'No verification code found'}
            
            record_id, stored_code, expiry, attempts = result
            
            # Check if too many attempts
            if attempts >= Config.MAX_VERIFICATION_ATTEMPTS:
                return {'success': False, 'message': 'Maximum verification attempts exceeded'}
            
            # Check if code expired
            if datetime.now() > datetime.fromisoformat(expiry):
                return {'success': False, 'message': 'Verification code has expired'}
            
            # Check if code matches
            if stored_code != code:
                # Increment attempts
                if verification_type == 'email':
                    cursor.execute('UPDATE verification_codes SET email_attempts = email_attempts + 1 WHERE id = ?', (record_id,))
                else:
                    cursor.execute('UPDATE verification_codes SET mobile_attempts = mobile_attempts + 1 WHERE id = ?', (record_id,))
                conn.commit()
                return {'success': False, 'message': 'Invalid verification code'}
            
            # Code is valid
            return {'success': True, 'message': 'Verification successful'}
            
        except Exception as e:
            print(f"Error verifying code: {str(e)}")
            return {'success': False, 'message': 'Verification failed'}
        finally:
            conn.close()
    
    def send_verification_codes(self, email, mobile_number, user_id=None):
        """Send verification codes to both email and mobile"""
        email_code = self.generate_verification_code()
        mobile_code = self.generate_verification_code()
        
        # Send codes
        email_sent = self.send_email_verification(email, email_code)
        mobile_sent = self.send_sms_verification(mobile_number, mobile_code)
        
        if email_sent and mobile_sent:
            # Store codes in database
            if self.store_verification_codes(email, mobile_number, email_code, mobile_code, user_id):
                return {'success': True, 'message': 'Verification codes sent successfully'}
            else:
                return {'success': False, 'message': 'Failed to store verification codes'}
        else:
            return {'success': False, 'message': 'Failed to send verification codes'}
    
    def mark_verified(self, email, mobile_number):
        """Mark email and mobile as verified in users table"""
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET email_verified = TRUE, mobile_verified = TRUE 
                WHERE email = ?
            ''', (email,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking as verified: {str(e)}")
            return False
        finally:
            conn.close()