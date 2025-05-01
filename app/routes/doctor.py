from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)

@doctor.route('/doctor/search', methods=['POST'])
def search_doctor():
    login = request.json.get('login')
    password = request.json.get('password')
    print(f"Login: {login}, Password: {password}")

    if not (login and password):
        return jsonify({'message': 'Login and password are required'}), 400

    try:
        doctor = Doctor.query.filter_by(login=login, password=password).first()
        if doctor:
            return jsonify(doctor.to_dict()), 200

        error_message = 'Doctor not found or incorrect password'
        return jsonify({'message': error_message}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        error_message = f'Database error: {str(e)}'
        print(f"Database error: {str(e)}")
        return jsonify({'message': error_message}), 500


@doctor.route('/doctor/current', methods=['GET'])  # Добавьте /doctor перед /current
def get_current_doctor():

    try:
        current_doctor = Doctor.query.first()

        if not current_doctor:
            return jsonify({'error': 'No doctors found'}), 404

        institution_name = current_doctor.institution.nameofinstitution if current_doctor.institution else "Неизвестное учреждение"

        return jsonify({
            'name': current_doctor.name,
            'secondname': current_doctor.secondname,
            'institutionname': institution_name,
            'institutioncode': current_doctor.institutioncode
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@doctor.route('/doctor/forgot/search', methods=['POST'])
def forgot_search_doctor():
    login = request.json.get('login')
    email = request.json.get('email')

    if not (login or email):
        return jsonify({'message': 'Login or email is required'}), 400

    try:
        doctor = Doctor.query.filter((Doctor.login == login) | (Doctor.email == email)).first()
        if doctor:
            return jsonify({'password': doctor.password}), 200

        error_message = 'Doctor not found'
        return jsonify({'message': error_message}), 404
    except SQLAlchemyError:
        error_message = 'Database error'
        return jsonify({'message': error_message}), 500


@doctor.route('/doctor/create', methods=['POST'])
def create_doctor():
    institutioncode = request.json.get('institutioncode')
    servicenumber = request.json.get('servicenumber')
    login = request.json.get('login')
    password = request.json.get('password')
    name = request.json.get('name')
    secondname = request.json.get('secondname')
    jobtitle = request.json.get('jobtitle')
    email = request.json.get('email')

    if not (institutioncode and servicenumber and login and password):
        return jsonify({'message': 'Institution code, service number, login, and password are required'}), 400

    doctor = Doctor(
        institutioncode=institutioncode,
        servicenumber=servicenumber,
        login=login,
        password=password,
        name=name,
        secondname=secondname,
        jobtitle=jobtitle,
        email=email
    )

    try:
        db.session.add(doctor)
        db.session.commit()
        return jsonify(doctor.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        error_message = f'Database error: {str(e)}'
        return jsonify({'message': error_message}), 500


@doctor.route('/doctor/update/<int:institutioncode>/<int:servicenumber>', methods=['POST'])
def update_doctor(institutioncode, servicenumber):
    doctor = Doctor.query.get_or_404((institutioncode, servicenumber))

    for field in request.json:
        if hasattr(doctor, field):
            setattr(doctor, field, request.json[field])

    try:
        db.session.commit()
        return jsonify(doctor.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        error_message = f'Database error: {str(e)}'
        return jsonify({'message': error_message}), 500