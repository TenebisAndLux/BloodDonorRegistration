from flask import Flask
from .extensions import db
from .extensions import migrate
from .config import Config

from .routes.main import main
from .routes.login import login
from .routes.forgot_login import forgot_login
from .routes.donor_list import donor_list
from .routes.add_donor import donor


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(main)
    app.register_blueprint(login)
    app.register_blueprint(forgot_login)
    app.register_blueprint(donor_list)
    app.register_blueprint(donor)


    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
