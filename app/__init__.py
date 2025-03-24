from flask import Flask
from .extensions import db
from .extensions import migrate
from .config import Config

from .routes.main import main
from .routes.login import login
from .routes.forgot_login import forgot_login
from .routes.add_donor import donor
from .routes.donor_list import donor_list
from .routes.doctor_info import doctor_info
from .routes.blood_bank import blood_bank
from .routes.hospital_info import hospital_info
from .routes.report_system import report_system
from .routes.information_system import information_system

from .routes.doctor import doctor
from .routes.medical_history import medical_history
from .routes.report import report
from .routes.blood_collections import blood_collection


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(doctor)
    app.register_blueprint(medical_history)
    app.register_blueprint(report)
    app.register_blueprint(blood_collection)

    app.register_blueprint(main)
    app.register_blueprint(login)
    app.register_blueprint(forgot_login)
    app.register_blueprint(information_system)
    app.register_blueprint(donor)
    app.register_blueprint(donor_list)
    app.register_blueprint(doctor_info)
    app.register_blueprint(blood_bank)
    app.register_blueprint(hospital_info)
    app.register_blueprint(report_system)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
