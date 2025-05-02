from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)


@doctor.route('/doctor/search', methods=['POST'])
def search_doctor():
    print("\n=== NEW AUTHENTICATION REQUEST ===")

    try:
        # Log raw incoming data
        raw_data = request.data.decode('utf-8')
        print(f"1. Received raw request data: {raw_data}")

        data = request.get_json()
        print(f"2. JSON data: {data}")

        if not data:
            print("ERROR: Missing JSON data")
            return jsonify({'error': 'JSON required'}), 400

        in_login = data.get('login')
        in_password = data.get('password')
        print(f"3. Input data - Login: '{in_login}', Password (length: {len(in_password) if in_password else 0} chars)")

        print(f"4. Searching doctor with login '{in_login}' in database...")
        doctor = Doctor.query.filter_by(login=in_login).first()

        if not doctor:
            print(f"ERROR: Doctor with login '{in_login}' not found")
            return jsonify({'error': 'User not found'}), 404

        print(f"5. Doctor found: ID={doctor.institutioncode}/{doctor.servicenumber}")
        print(f"6. Password hash from DB: {doctor.password}")

        db_hash = doctor.password
        print("CHECK RESULT:", check_password_hash(db_hash, 'pass123'))

        print("7. Verifying password...")
        is_password_valid = check_password_hash(doctor.password, in_password)
        print(f"8. Password verification result: {'SUCCESS' if is_password_valid else 'FAILURE'}")

        if not is_password_valid:
            print(f"9. AUTH ERROR: Invalid password for '{in_login}'")
            print(f"   Entered password: '{in_password}'")
            print(f"   Password length: {len(in_password)} chars")
            print(f"   DB hash: {doctor.password}")
            return jsonify({'error': 'Invalid credentials'}), 401

        print(f"10. AUTH SUCCESS for '{in_login}'")
        return jsonify({
            'institutioncode': doctor.institutioncode,
            'servicenumber': doctor.servicenumber,
            'name': doctor.name,
            'secondname': doctor.secondname
        })

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


@doctor.route('/doctor/current', methods=['GET'])
@login_required
def get_current_doctor():
    try:
        institution_name = current_user.institution.nameofinstitution if current_user.institution else "Неизвестное учреждение"

        return jsonify({
            'name': current_user.name,
            'secondname': current_user.secondname,
            'institutionname': institution_name,
            'institutioncode': current_user.institutioncode
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