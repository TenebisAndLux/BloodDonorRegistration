from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user, login_required
from app.services.email_service import send_password_email
from ..extensions import db
from ..models.doctor import Doctor
from werkzeug.security import generate_password_hash
import secrets
import string

doctor = Blueprint('doctor', __name__)


@doctor.route('/doctor/search', methods=['POST'])
def search_doctor():
    return 0

@doctor.route('/doctor/forgot/search', methods=['POST'])
def forgot_search_doctor():
    try:
        if not request.data:
            return jsonify({'message': 'Пустое тело запроса'}), 400

        try:
            data = request.get_json(force=True)
        except Exception:
            return jsonify({'message': 'Некорректный JSON'}), 400

        login = data.get('login') or data.get('username')
        email = data.get('email')

        if not (login and email):
            return jsonify({'message': 'Требуется логин и email'}), 400

        doctor = Doctor.query.filter_by(login=login).first()
        if not doctor:
            return jsonify({'message': 'Пользователь не найден'}), 404

        if doctor.email.lower() != email.lower():
            return jsonify({'message': 'Email не совпадает с указанным при регистрации'}), 400

        # Генерация временного пароля
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        hashed_password = generate_password_hash(temp_password, method='scrypt')

        # Обновление пароля в базе данных
        doctor.password = hashed_password
        db.session.commit()

        # Отправка временного пароля по email
        if send_password_email(doctor.email, temp_password):
            return jsonify({'message': 'Временный пароль отправлен на ваш email'}), 200
        else:
            return jsonify({'message': 'Ошибка при отправке письма'}), 500

    except Exception:
        return jsonify({'message': 'Ошибка сервера'}), 500

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