from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TimeField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class AppointmentForm(FlaskForm):
    appointment_id = IntegerField('Appointment ID', validators=[DataRequired()])
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    patient_email = StringField('Patient Email', validators=[DataRequired(), Email()])
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', validators=[DataRequired()])
    specialist = SelectField('Specialist', validators=[DataRequired()])
    problem = TextAreaField('Problem', validators=[DataRequired()])
    submit = SubmitField('Update Appointment')