from flask import Blueprint, jsonify, request, render_template, current_app
from flask_login import login_required, current_user
from ..models import Doctor, MedicalInstitution
from ..extensions import db
from .. import MagmaCipher
from ..utils.decorators import role_required

doctor_info = Blueprint('doctor_info', __name__)


@doctor_info.route('/doctor/list')
@login_required
@role_required('admin')
def index():
    return render_template('main/doctor_index.html')


@doctor_info.route('/doctor/list/all')
@login_required
@role_required('admin')
def get_all_doctors():
    try:
        doctors = Doctor.query.all()
        doctors_list = []

        for doctor in doctors:
            institution_name = doctor.institution.nameofinstitution if doctor.institution else "Неизвестное учреждение"
            doctor_dict = {
                'institutioncode': doctor.institutioncode,
                'servicenumber': doctor.servicenumber,
                'name': doctor.name,
                'secondname': doctor.secondname,
                'jobtitle': doctor.jobtitle,
                'role': doctor.role,
                'login': doctor.login,
                'email': doctor.email,
                'institutionname': institution_name
            }
            doctors_list.append(doctor_dict)

        return jsonify(doctors_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_info.route('/doctor/list/search', methods=['POST'])
@login_required
@role_required('admin')
def search_doctors():
    try:
        data = request.get_json()
        cipher = MagmaCipher()

        # Шифруем параметры поиска, которые хранятся в зашифрованном виде
        encrypted_params = {}
        if 'name' in data and data['name']:
            encrypted_params['_name'] = cipher.encrypt(data['name'].encode('utf-8'), mode='ECB').hex()
        if 'secondname' in data and data['secondname']:
            encrypted_params['_secondname'] = cipher.encrypt(data['secondname'].encode('utf-8'), mode='ECB').hex()
        if 'jobtitle' in data and data['jobtitle']:
            encrypted_params['_jobtitle'] = cipher.encrypt(data['jobtitle'].encode('utf-8'), mode='ECB').hex()

        query = db.session.query(Doctor, MedicalInstitution).outerjoin(
            MedicalInstitution, Doctor.institutioncode == MedicalInstitution.institutioncode
        )

        # Добавляем условия поиска
        if '_name' in encrypted_params:
            query = query.filter(Doctor._name == encrypted_params['_name'])
        if '_secondname' in encrypted_params:
            query = query.filter(Doctor._secondname == encrypted_params['_secondname'])
        if '_jobtitle' in encrypted_params:
            query = query.filter(Doctor._jobtitle == encrypted_params['_jobtitle'])
        if 'servicenumber' in data and data['servicenumber']:
            query = query.filter(Doctor.servicenumber == data['servicenumber'])

        results = query.all()

        doctors_list = []
        for doctor, institution in results:
            doctor_dict = doctor.to_dict()

            institution_name = 'Неизвестное учреждение'
            if institution and institution._nameofinstitution:
                try:
                    decrypted = cipher.decrypt(bytes.fromhex(institution._nameofinstitution), mode='ECB')
                    institution_name = decrypted.decode('utf-8')
                except Exception as e:
                    print(f"[Decryption error] Institution name: {e}")
                    institution_name = 'Ошибка расшифровки'

            doctor_dict['institutionname'] = institution_name
            doctors_list.append(doctor_dict)
        return jsonify(doctors_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_info.route('/doctor/get')
@login_required
@role_required('admin')
def get_doctor():
    try:
        institutioncode = request.args.get('institutioncode')
        servicenumber = request.args.get('servicenumber')

        if not institutioncode or not servicenumber:
            return jsonify({'error': 'Необходимы institutioncode и servicenumber'}), 400

        doctor = Doctor.query.filter_by(
            institutioncode=institutioncode,
            servicenumber=servicenumber
        ).first()

        if not doctor:
            return jsonify({'error': 'Врач не найден'}), 404

        return jsonify(doctor.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_info.route('/doctor/add', methods=['POST'])
@login_required
@role_required('admin')
def add_doctor():
    try:
        data = request.get_json()
        cipher = current_app.config.get('ENCRYPTION_CIPHER')

        # Проверка обязательных полей
        required_fields = ['name', 'secondname', 'jobtitle', 'role', 'login', 'password', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400

        # Проверка уникальности логина
        encrypted_login = cipher.encrypt(data['login'].encode('utf-8'), mode='ECB').hex()
        existing_doctor = Doctor.query.filter_by(_login=encrypted_login).first()
        if existing_doctor:
            return jsonify({'error': 'Логин уже используется'}), 400

        # Генерация табельного номера
        last_doctor = Doctor.query.filter_by(institutioncode=current_user.institutioncode)\
                                .order_by(Doctor.servicenumber.desc()).first()
        new_servicenumber = last_doctor.servicenumber + 1 if last_doctor else 1

        # Создание нового врача
        new_doctor = Doctor(
            institutioncode=current_user.institutioncode,
            servicenumber=new_servicenumber,
            _role=cipher.encrypt(data['role'].encode('utf-8'), mode='ECB').hex(),
            _name=cipher.encrypt(data['name'].encode('utf-8'), mode='ECB').hex(),
            _secondname=cipher.encrypt(data['secondname'].encode('utf-8'), mode='ECB').hex(),
            _jobtitle=cipher.encrypt(data['jobtitle'].encode('utf-8'), mode='ECB').hex(),
            _login=encrypted_login,
            _email=cipher.encrypt(data['email'].encode('utf-8'), mode='ECB').hex()
        )
        new_doctor.set_password(data['password'])

        db.session.add(new_doctor)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Врач успешно добавлен',
            'doctor': new_doctor.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding doctor: {str(e)}")
        return jsonify({'error': str(e)}), 500


@doctor_info.route('/doctor/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_doctor():
    try:
        data = request.get_json()

        required_fields = ['institutioncode', 'servicenumber']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Необходимы institutioncode и servicenumber'}), 400

        doctor = Doctor.query.filter_by(
            institutioncode=data['institutioncode'],
            servicenumber=data['servicenumber']
        ).first()

        if not doctor:
            return jsonify({'error': 'Врач не найден'}), 404

        # Обновление полей
        if 'name' in data:
            doctor.name = data['name']
        if 'secondname' in data:
            doctor.secondname = data['secondname']
        if 'jobtitle' in data:
            doctor.jobtitle = data['jobtitle']
        if 'role' in data:
            doctor.role = data['role']
        if 'login' in data:
            # Проверка уникальности нового логина
            if data['login'] != doctor.login:
                existing_doctor = Doctor.query.filter_by(_login=data['login']).first()
                if existing_doctor:
                    return jsonify({'error': 'Логин уже используется'}), 400
            doctor.login = data['login']
        if 'password' in data and data['password']:
            doctor.set_password(data['password'])
        if 'email' in data:
            doctor.email = data['email']

        db.session.commit()

        return jsonify({'success': True, 'message': 'Данные врача обновлены'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@doctor_info.route('/doctor/dismiss', methods=['POST'])
@login_required
@role_required('admin')
def dismiss_doctor():
    try:
        data = request.get_json()

        required_fields = ['institutioncode', 'servicenumber', 'transfer_institutioncode', 'transfer_servicenumber']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400

        # Проверка, что врач существует
        doctor = Doctor.query.filter_by(
            institutioncode=data['institutioncode'],
            servicenumber=data['servicenumber']
        ).first()

        if not doctor:
            return jsonify({'error': 'Врач не найден'}), 404

        # Проверка, что врач для передачи существует
        transfer_doctor = Doctor.query.filter_by(
            institutioncode=data['transfer_institutioncode'],
            servicenumber=data['transfer_servicenumber']
        ).first()

        if not transfer_doctor:
            return jsonify({'error': 'Врач для передачи не найден'}), 404

        db.session.delete(doctor)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Врач уволен, записи переданы'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500