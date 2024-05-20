from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)


@doctor.route('/doctor/search', methods=['POST'])
def search_doctor():
    login = request.json.get('login')
    password = request.json.get('password')

    if not (login and password):
        return jsonify({'message': 'Login and password are required'}), 400

    try:
        doctor = Doctor.query.filter_by(login=login, password=password).first()
        if doctor:
            return jsonify(doctor.to_dict()), 200

        error_message = 'Doctor not found or incorrect password'
        return jsonify({'message': error_message}), 404
    except SQLAlchemyError:
        error_message = 'Database error'
        return jsonify({'message': error_message}), 500


@doctor.route('/doctor/create', methods=['POST'])
def create_doctor():
    doctor = Doctor(login=request.json.get('login'),
                    password=request.json.get('password'),
                    first_name=request.json.get('first_name'),
                    last_name=request.json.get('last_name'),
                    position=request.json.get('position'),
                    email=request.json.get('email'))
    db.session.add(doctor)
    db.session.commit()
    return jsonify(doctor.to_dict())


@doctor.route('/doctor/update/<int:doctor_id>', methods=['POST'])
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    for field in doctor.to_dict():
        if field in request.json:
            setattr(doctor, field, request.json[field])
    db.session.commit()
    return jsonify(doctor.to_dict())
