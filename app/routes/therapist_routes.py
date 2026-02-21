from flask import Blueprint, render_template, flash, redirect, url_for,session,request
from app.models import User,Therapist
from app.extensions import db


therapist_bp = Blueprint('therapist', __name__)

@therapist_bp.route('/dashboard')
def therapist_dashboard():
    if 'email' in session:
        therapist = User.query.filter_by(email=session['email']).first()
        if therapist:
            return render_template('therapist/therapist_dashboard.html', user_profile=therapist,active_page='therapist_dashboard')
        else:
            flash("User not found", "danger")
            return redirect(url_for('auth.login'))
    else:
        flash("You are not logged in", "danger")
        return redirect(url_for('auth.login'))

# Route to display the therapist list
@therapist_bp.route('/therapist_list')
def therapist_list():
    therapists = Therapist.query.all()  # Fetch all therapists
    print(f"Therapists fetched: {therapists}")  # Debugging: Print therapists to the console
    return render_template('therapist/therapist_list.html', therapists=therapists, active_page='therapist_list')


# Route to delete a therapist
@therapist_bp.route('/delete_therapist/<int:therapist_id>', methods=['GET'])
def delete_therapist(therapist_id):
    therapist = Therapist.query.get_or_404(therapist_id)
    db.session.delete(therapist)
    db.session.commit()
    flash('Therapist deleted successfully!', 'success')
    return redirect(url_for('therapist.therapist_list'))


@therapist_bp.route('/card')
def therapist_card():
    return render_template('therapist/therapist_card.html')

@therapist_bp.route('/profile')
def therapist_profiles():
    return render_template('therapist/therapist_profile.html',active_page='therapist_profiles')
