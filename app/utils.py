from flask_mail import Message
from flask import current_app
from app import mail
import re
import secrets

# Utility: Send OTP Email
def send_otp_email(email, otp):
    """
    Sends an OTP email to the specified email address.
    
    :param email: The recipient's email address.
    :param otp: The OTP code to send.
    """
    try:
        subject = "Your OTP for Verification"
        sender = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
        recipients = [email]
        body = f"Hello User, We are from Speechcare Hub \n\nYour OTP for verification is: {otp}\n\nThis OTP will expire in 5 minutes."
        
        msg = Message(subject=subject, sender=sender, recipients=recipients, body=body)
        mail.send(msg)
        current_app.logger.info(f"OTP email sent to {email}")
    except Exception as e:
        current_app.logger.error(f"Error sending OTP email to {email}: {e}")
        raise e

# Utility: Validate Email Format
def is_valid_email(email):
    """
    Validates if the given email has a valid format.
    
    :param email: The email address to validate.
    :return: True if valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Utility: Generate Random OTP
def generate_otp(length=6):
    """
    Generates a random OTP of the specified length.
    
    :param length: The length of the OTP (default is 6).
    :return: A string representing the OTP.
    """
    if length <= 0:
        raise ValueError("OTP length must be greater than 0")
    return ''.join(secrets.choice("0123456789") for _ in range(length))
