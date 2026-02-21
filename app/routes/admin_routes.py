from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from app.models import User, Therapist, Patient
from werkzeug.security import generate_password_hash
from app.extensions import db

admin_bp = Blueprint('admin', __name__)

# Route for admin dashboard
@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        if user:
            return render_template('admin/admin_dashboard.html', active_page='admin_dashboard')
        else:
            flash("User not found", "danger")
            return redirect(url_for('auth.login'))  # Redirect if user is not found
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for('auth.login'))


# Route to display the edit patient profile page
@admin_bp.route('/edit_patient', methods=['GET', 'POST'])
def edit_patient():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        patient = Patient.query.get(patient_id)
        if patient:
            return render_template('admin/edit_patient.html', patient=patient)
        else:
            flash('Patient not found!', 'danger')
            return redirect(url_for('admin.edit_patient'))
    return render_template('admin/edit_patient.html', active_page='edit_patient')


# Route to handle the form submission for updating patient data
@admin_bp.route('/update_patient/<int:patient_id>', methods=['POST'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.first_name = request.form.get('first_name')
    patient.last_name = request.form.get('last_name')
    patient.age = request.form.get('age')
    patient.gender = request.form.get('gender')
    patient.phone_number = request.form.get('phone_number')
    patient.state = request.form.get('state')
    patient.city = request.form.get('city')
    db.session.commit()
    flash('Patient profile updated successfully!', 'success')
    return redirect(url_for('admin.edit_patient'))


# Route to add a new therapist
@admin_bp.route('/add_therapist', methods=['GET', 'POST'])
def add_therapist():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        state = request.form.get('state')
        city = request.form.get('city')
        designation = request.form.get('designation')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate passwords
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('admin.add_therapist'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('admin.add_therapist'))

        # Create a new User
        new_user = User(
            email=email,
            password=generate_password_hash(password),
            role='therapist'  # Set role to therapist
        )
        db.session.add(new_user)
        db.session.commit()

        # Create a new Therapist
        new_therapist = Therapist(
            user_id=new_user.id,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            phone_number=phone_number,
            state=state,
            city=city,
            designation=designation
        )
        db.session.add(new_therapist)
        db.session.commit()

        flash('Therapist profile created successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('admin/add_therapist.html', active_page='add_therapist')



# Route to view therapist details
@admin_bp.route('/view_therapist/<int:therapist_id>', methods=['GET'])
def view_therapist(therapist_id):
    therapist = Therapist.query.get_or_404(therapist_id)
    return render_template('admin/view_therapist.html', therapist=therapist, active_page='view_therapist')


# Route to edit therapist details
@admin_bp.route('/edit_therapist', methods=['GET', 'POST'])
def edit_therapist():
    if request.method == 'POST':
        therapist_id = request.form.get('therapist_id')
        therapist = Therapist.query.get(therapist_id)
        if therapist:
            return render_template('admin/edit_therapist.html', therapist=therapist)
        else:
            flash('Therapist not found!', 'danger')
            return redirect(url_for('admin.edit_therapist'))
    return render_template('admin/edit_therapist.html', active_page='edit_therapist')


# Route to handle the form submission for updating therapist data
@admin_bp.route('/update_therapist/<int:therapist_id>', methods=['POST'])
def update_therapist(therapist_id):
    therapist = Therapist.query.get_or_404(therapist_id)
    therapist.first_name = request.form.get('first_name')
    therapist.last_name = request.form.get('last_name')
    therapist.age = request.form.get('age')
    therapist.gender = request.form.get('gender')
    therapist.phone_number = request.form.get('phone_number')
    therapist.state = request.form.get('state')
    therapist.city = request.form.get('city')
    therapist.designation = request.form.get('designation')
    db.session.commit()
    flash('Therapist profile updated successfully!', 'success')
    return redirect(url_for('admin.edit_therapist'))