from flask import Flask
from .extensions import db
from .config import Config

from .routes import doctor
from .routes import donor
from .routes import blood_collections
from .routes import medical_history
from .routes import report
from .routes import main


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(doctor)
    app.register_blueprint(donor)
    app.register_blueprint(blood_collections)
    app.register_blueprint(medical_history)
    app.register_blueprint(report)
    app.register_blueprint(main)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
