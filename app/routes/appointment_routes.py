from flask import Blueprint, render_template,request,redirect, url_for, flash
from app.models import Appointment, Patient, Therapist
from app.forms import AppointmentForm  # Ensure you have this form defined
from app import db
from sqlalchemy.orm import joinedload

appointment_bp = Blueprint('appointment', __name__)

from app.forms import AppointmentForm


@appointment_bp.route('/list')
def appoint_list():
    # Fetch all appointments with patient and therapist details
    appointments = db.session.query(Appointment) \
        .join(Patient, Appointment.patient_id == Patient.id) \
        .join(Therapist, Appointment.therapist_id == Therapist.id) \
        .all()

    return render_template('appointment/appoint_list.html', appointments=appointments, active_page='appoint_list')


@appointment_bp.route('/admin/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    form = AppointmentForm()

    # Populate therapist choices dynamically
    form.therapist_id.choices = [(t.id, f"{t.first_name} {t.last_name}") for t in Therapist.query.all()]
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") for p in Patient.query.all()]

    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            therapist_id=form.therapist_id.data,
            appointment_date=form.appointment_date.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointment.appoint_list'))  # Redirect to the appointment list

    return render_template('admin/add_appointment.html', form=form,active_page='add_appointment')


@appointment_bp.route('/admin/edit_appointment', methods=['GET', 'POST'])
def edit_appointment():
    form = AppointmentForm()

    if request.method == 'POST':
        # Check if the form is submitted with an appointment_id
        appointment_id = form.appointment_id.data

        if appointment_id:
            # Fetch the appointment from the database
            appointment = Appointment.query.get(appointment_id)

            if appointment:
                # Fetch related patient and therapist details
                patient = Patient.query.get(appointment.patient_id)
                therapist = Therapist.query.get(appointment.therapist_id)

                # Auto-fill the form fields
                form.patient_name.data = f"{patient.first_name} {patient.last_name}"
                form.age.data = patient.age
                form.gender.data = patient.gender
                form.patient_email.data = patient.email
                form.appointment_date.data = appointment.appointment_date
                form.appointment_time.data = appointment.appointment_time
                form.specialist.data = f"{therapist.first_name} {therapist.last_name}"
                form.problem.data = appointment.problem
            else:
                flash('Appointment not found!', 'danger')

    return render_template('appointment/edit_appoint.html', form=form, active_page='edit_appointment')


@appointment_bp.route('/admin/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointment.appoint_list'))  # Redirect to the appointment list

@appointment_bp.route('therpay_plan')
def therapy_plan():
    return render_template('appointment/therapy_plan.html', active_page='therapy_plan')