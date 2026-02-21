from flask import Blueprint, render_template, flash, redirect, url_for,session,request
from app.models import User,Patient
from app.extensions import db

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/User/<int:id>')
def patient_profile(id):
    if 'email' not in session:
        flash("You are not logged in", "danger")
        return redirect(url_for('auth.login'))

    user_profile = User.query.get(id)
    if not user_profile:
        flash("User not found.", "danger")
        return redirect(url_for('auth.login'))

    return render_template('patient/patient_dashboard.html', user_profile=user_profile)



# Route for patinet dashboard
@patient_bp.route('/patient_dashboard')
def patient_dashboard():
    if 'email' in session:
        patient = User.query.filter_by(email=session['email']).first()
        if patient:
            return render_template('patient/patient_dashboard.html', user_profile=patient,active_page='patient_dashboard')
        else:
            flash("User not found", "danger")
            return redirect(url_for('auth.login'))  # Redirect if user is not found
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for('auth.login'))


@patient_bp.route('/list')
def patient_list():
    patients = Patient.query.all()  # Fetch all patients
    print(f"Patients fetched: {patients}")
    return render_template('patient/patient_list.html', patients=patients,active_page='patient_list')



# Route to delete a patient
@patient_bp.route('/delete_patient/<int:patient_id>', methods=['GET'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patient.patient_list'))

@patient_bp.route('/patient_profiles')
def patient_profiles():
    return render_template('patient/patient_profile.html',active_page='patient_profiles')


