from flask import Blueprint, jsonify, request, current_app, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from ..models import MedicalInstitution
from ..extensions import db
from .. import MagmaCipher
from ..utils.decorators import role_required

medical_institution = Blueprint('medical_institution', __name__)


@medical_institution.route('/medical_institution/list')
@login_required
@role_required('admin')
def index():
    return render_template('main/medical_institution_index.html')
@medical_institution.route('/medical_institution/list/all')
@login_required
@role_required('admin')
def list_institutions():
    try:
        institutions = MedicalInstitution.query.all()
        result = []

        for inst in institutions:
            result.append({
                'institutioncode': inst.institutioncode,
                'nameofinstitution': inst.nameofinstitution,
                'address': inst.address,
                'contactphonenumber': inst.contactphonenumber,
                'email': inst.email,
                'typeofinstitution': inst.typeofinstitution
            })

        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error listing institutions: {str(e)}")
        return jsonify({'error': str(e)}), 500


@medical_institution.route('/medical_institution/list/search', methods=['POST'])
@login_required
@role_required('admin')
def search_institutions():
    try:
        data = request.get_json()
        cipher = current_app.config.get('ENCRYPTION_CIPHER')

        query = MedicalInstitution.query

        if data.get('nameofinstitution'):
            enc_name = cipher.encrypt(data['nameofinstitution'].encode('utf-8'), mode='ECB').hex()
            query = query.filter(MedicalInstitution._nameofinstitution == enc_name)
        if data.get('typeofinstitution'):
            enc_type = cipher.encrypt(data['typeofinstitution'].encode('utf-8'), mode='ECB').hex()
            query = query.filter(MedicalInstitution._typeofinstitution == enc_type)
        if data.get('address'):
            enc_addr = cipher.encrypt(data['address'].encode('utf-8'), mode='ECB').hex()
            query = query.filter(MedicalInstitution._address == enc_addr)
        if data.get('contactphonenumber'):
            enc_phone = cipher.encrypt(data['contactphonenumber'].encode('utf-8'), mode='ECB').hex()
            query = query.filter(MedicalInstitution._contactphonenumber == enc_phone)

        institutions = query.all()
        result = []

        for inst in institutions:
            result.append({
                'institutioncode': inst.institutioncode,
                'nameofinstitution': inst.nameofinstitution,
                'address': inst.address,
                'contactphonenumber': inst.contactphonenumber,
                'email': inst.email,
                'typeofinstitution': inst.typeofinstitution
            })

        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error searching institutions: {str(e)}")
        return jsonify({'error': str(e)}), 500


@medical_institution.route('/medical_institution/add', methods=['POST'])
@login_required
@role_required('admin')
def add_institution():
    try:
        data = request.get_json()
        cipher = current_app.config.get('ENCRYPTION_CIPHER')

        # Генерация нового institutioncode
        max_code = db.session.query(func.max(MedicalInstitution.institutioncode)).scalar() or 0
        new_code = max_code + 1

        new_institution = MedicalInstitution(
            institutioncode=new_code,
            _nameofinstitution=cipher.encrypt(data['nameofinstitution'].encode('utf-8'), mode='ECB').hex(),
            _address=cipher.encrypt(data['address'].encode('utf-8'), mode='ECB').hex(),
            _contactphonenumber=cipher.encrypt(data['contactphonenumber'].encode('utf-8'), mode='ECB').hex(),
            _email=cipher.encrypt(data['email'].encode('utf-8'), mode='ECB').hex(),
            _typeofinstitution=cipher.encrypt(data['typeofinstitution'].encode('utf-8'), mode='ECB').hex()
        )

        db.session.add(new_institution)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Учреждение успешно добавлено',
            'institutioncode': new_code
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding institution: {str(e)}")
        return jsonify({'error': 'Ошибка при добавлении учреждения. Проверьте данные.'}), 500


@medical_institution.route('/medical_institution/<int:institutioncode>', methods=['GET'])
@login_required
@role_required('admin')
def get_institution(institutioncode):
    try:
        institution = MedicalInstitution.query.get_or_404(institutioncode)

        return jsonify({
            'institutioncode': institution.institutioncode,
            'nameofinstitution': institution.nameofinstitution,
            'address': institution.address,
            'contactphonenumber': institution.contactphonenumber,
            'email': institution.email,
            'typeofinstitution': institution.typeofinstitution
        })
    except Exception as e:
        current_app.logger.error(f"Error getting institution: {str(e)}")
        return jsonify({'error': str(e)}), 500


@medical_institution.route('/medical_institution/<int:institutioncode>', methods=['PUT'])
@login_required
@role_required('admin')
def update_institution(institutioncode):
    try:
        data = request.get_json()
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        institution = MedicalInstitution.query.get_or_404(institutioncode)

        # Обновляем поля
        if 'nameofinstitution' in data:
            institution._nameofinstitution = cipher.encrypt(data['nameofinstitution'].encode('utf-8'), mode='ECB').hex()
        if 'address' in data:
            institution._address = cipher.encrypt(data['address'].encode('utf-8'), mode='ECB').hex()
        if 'contactphonenumber' in data:
            institution._contactphonenumber = cipher.encrypt(data['contactphonenumber'].encode('utf-8'),
                                                             mode='ECB').hex()
        if 'email' in data:
            institution._email = cipher.encrypt(data['email'].encode('utf-8'), mode='ECB').hex()
        if 'typeofinstitution' in data:
            institution._typeofinstitution = cipher.encrypt(data['typeofinstitution'].encode('utf-8'), mode='ECB').hex()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Данные учреждения обновлены'
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating institution: {str(e)}")
        return jsonify({'error': str(e)}), 500