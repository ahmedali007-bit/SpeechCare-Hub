from flask import Flask
from config import Config
from app.extensions import db, mail, login_manager
from app.models import User
from app.models import User
from werkzeug.security import generate_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

     # Set the login view for unauthorized users
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.patient_routes import patient_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.therapist_routes import therapist_bp
    from app.routes.appointment_routes import appointment_bp
    from app.routes.general_routes import general_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(therapist_bp, url_prefix='/therapist')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(general_bp)
    app.register_blueprint(errors_bp)

    # Initialize database
    with app.app_context():
        admin_user = User.query.filter_by(email='ahmedali@admin.com').first()

        if not admin_user:
            # Create the admin user
            admin_user = User(
                id=1,
                email='ahmedali@admin.com',
                role='Admin',
                password=generate_password_hash('59111763890290900676493')
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        db.create_all()

    return app
