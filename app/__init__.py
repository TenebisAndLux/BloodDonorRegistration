from flask import Flask, request
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf

from app.services.email_service import init_mail

from .config import Config

from .extensions import (db)
from .extensions import migrate


from .models import Doctor
from .routes.main import main
from .routes.auth import auth
from .routes.forgot_login import forgot_login
from .routes.donor import donor
from .routes.donor_list import donor_list
from .routes.doctor_info import doctor_info
from .routes.blood_bank import blood_bank
from .routes.hospital_info import hospital_info
from .routes.report_system import report_system
from .routes.information_system import information_system
from .routes.doctor import doctor
from .routes.medical_history import medical_history
from .routes.blood_collections import blood_collection


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CSRFProtect(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = 'auth.login'

    CORS(app, supports_credentials=True, expose_headers=['Set-Cookie'])
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            parts = user_id.split('|')
            return Doctor.query.filter_by(
                institutioncode=parts[0],
                servicenumber=parts[1]
            ).first()
        except Exception as e:
            app.logger.error(f"Error loading user: {str(e)}")
            return None

    app.register_blueprint(auth)
    app.register_blueprint(doctor)
    app.register_blueprint(medical_history)
    app.register_blueprint(blood_collection)
    app.register_blueprint(main)
    app.register_blueprint(forgot_login)
    app.register_blueprint(information_system)
    app.register_blueprint(donor)
    app.register_blueprint(donor_list)
    app.register_blueprint(doctor_info)
    app.register_blueprint(blood_bank)
    app.register_blueprint(hospital_info)
    app.register_blueprint(report_system)

    db.init_app(app)
    init_mail(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
