from flask import Flask
from .extensions import db
from .config import Config

from .routes.doctor import doctor
from .routes.donor import donor
from .routes.blood_collections import blood_collection
from .routes.medical_history import medical_history
from .routes.report import report
from .routes.main import main
from .routes.login import login


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #app.register_blueprint(doctor)
    #app.register_blueprint(donor)
    #app.register_blueprint(blood_collection)
    #app.register_blueprint(medical_history)
    #app.register_blueprint(report)
    app.register_blueprint(main)
    app.register_blueprint(login)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
