from flask import Blueprint
from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)


@doctor.route('/login/doctor/create')
def create_doctor():
    doctor = Doctor()
    db.session.add(doctor)
    db.session.commit()
    return 'doctor Created Susses'
