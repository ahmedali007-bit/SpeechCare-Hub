from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from app.models import User,Patient
from app.utils import send_otp_email 
from app import db
import random
import re
import logging

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routes login 
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            login_user(user)  # Log the user in
            session['email'] = user.email
            session['role'] = user.role  # Store the user's role in the session

            # Redirect based on role
            if user.role == 'Admin' and user.email == 'ahmedali@admin.com' and user.id == 1:  
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'therapist':
                return redirect(url_for('therapist.therapist_dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient.patient_dashboard'))
            else:
                flash('You do not have access to any dashboard.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', active_page='login')


@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        state = request.form.get('state')
        city = request.form.get('city')

        # Validate passwords
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.sign_up'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.sign_up'))

        # Create a new User
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            role='patient'  # Default role for sign-up
        )
        db.session.add(new_user)
        db.session.commit()

        # Create a new Patient
        new_patient = Patient(
            user_id=new_user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            phone_number=phone_number,
            state=state,
            city=city
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', active_page='sign_up')

#route forget password
@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("This email is not registered.", 'danger')
            return redirect(url_for('auth.forgot_password'))

        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = datetime.now(timezone.utc) + timedelta(minutes=5)
        session['email'] = email

        try:
            send_otp_email(email, otp)
            flash("OTP sent to your email.", 'success')
            return redirect(url_for('auth.otp_verification'))
        except Exception as e:
            flash("Failed to send OTP. Try again.", 'danger')
            print(f"Error: {e}")
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forget password.html')

#route otp verification
@auth_bp.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if request.method == 'POST':
        otp = ''.join([request.form.get(f'otp_digit_{i}') for i in range(1, 7)])  # Collect all digits
        if 'otp' not in session or session['otp'] != int(otp):
            flash("Invalid OTP.", 'danger')
            return redirect(url_for('auth.otp_verification'))

        if datetime.now(timezone.utc) > session['otp_expiry']:
            flash("OTP expired.", 'danger')
            return redirect(url_for('auth.forgot_password'))

        flash("OTP verified. You can now reset your password.", 'success')
        return redirect(url_for('auth.new_password'))

    return render_template('auth/OTP Verification.html')

@auth_bp.route('/resend_otp', methods=['GET'])
def resend_otp():
    if 'email' not in session:
        flash("Session expired. Please try again.", 'danger')
        return redirect(url_for('auth.forgot_password'))

    try:
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = datetime.now(timezone.utc) + timedelta(minutes=5)

        send_otp_email(session['email'], otp)
        flash("OTP resent to your email.", 'success')
    except Exception as e:
        flash("Failed to resend OTP. Please try again.", 'danger')
        print(f"Error: {e}")

    return redirect(url_for('auth.otp_verification'))

#route new password
@auth_bp.route('/new_password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", 'danger')
            return redirect(url_for('auth.new_password'))

        user = User.query.filter_by(email=session.get('email')).first()
        if not user:
            flash("Session expired. Please try again.", 'danger')
            return redirect(url_for('auth.forgot_password'))

        try:
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            flash("Password reset successfully. Please log in.", 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Error resetting password.", 'danger')
            print(f"Error: {e}")
            return redirect(url_for('auth.new_password'))

    return render_template('auth/new password.html')