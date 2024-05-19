from flask import Blueprint

from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)


@doctor.route('/doctor/<name>')
def create_donor(name):
    doctor = Doctor(name=name)
    db.session.add(doctor)
    db.session.commit()
    return 'Doctor be added'
