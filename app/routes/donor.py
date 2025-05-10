from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from werkzeug.exceptions import NotFound
from sqlalchemy import cast, String, text

from .. import MagmaCipher
from ..models.doctor import Doctor
from ..extensions import db
from ..models import MedicalInstitution, DonorMedicalExaminationResults, DoctorDonor, DonorDoctor, MedicalHistory
from ..models.blood_collection import BloodCollection
from ..models.blood_collection_type import BloodCollectionType
from ..models.blood_supply import BloodSupply
from ..models.donor import Donor
from ..models.medical_examination import MedicalExamination

donor = Blueprint('donor', __name__)

@donor.route('/donor/add', methods=['POST'])
def create():
    data = request.get_json()

    donor = Donor(
        passportdata=data.get('passportdata'),
        institutioncode=data.get('institutioncode'),
        historynumber=data.get('historynumber'),
        name=data.get('name'),
        secondname=data.get('secondname'),
        surname=data.get('surname'),
        birthday=data.get('birthday'),
        gender=data.get('gender'),
        address=data.get('address'),
        phonenumber=data.get('phonenumber'),
        polis=data.get('polis'),
        bloodgroup=data.get('bloodgroup'),
        rhfactor=data.get('rhfactor')
    )

    try:
        db.session.add(donor)
        db.session.commit()
        return jsonify({'message': 'Донор успешно создан. ', 'id': donor.passportdata}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Данный донор есть в системе.'}), 500

@donor.route('/donor/edit', methods=['POST'])
def edit_donor():
    data = request.get_json()

    old_passport = data.get('old_passportdata')
    old_institution = data.get('old_institutioncode')
    new_passport = data.get('passportdata')
    new_institution = data.get('institutioncode')

    if not old_passport or not old_institution:
        return jsonify({'message': 'Не указаны исходные паспортные данные'}), 400

    donor = Donor.query.get_or_404((old_passport, old_institution))

    try:
        with db.session.begin_nested():
            # Проверяем, изменились ли ключевые поля
            if new_passport != old_passport or new_institution != old_institution:
                # Проверяем, нет ли уже донора с новыми данными
                if Donor.query.get((new_passport, new_institution)):
                    return jsonify({'message': 'Донор с такими паспортными данными уже существует'}), 400

                # Обновляем все связанные таблицы в одной транзакции
                related_tables = [
                    MedicalExamination,
                    DonorMedicalExaminationResults,
                    DoctorDonor,
                    DonorDoctor,
                    BloodCollection
                ]

                for table in related_tables:
                    db.session.query(table).filter_by(
                        passportdata=old_passport,
                        institutioncode=old_institution
                    ).update({
                        'passportdata': new_passport,
                        'institutioncode': new_institution
                    })

                # Для MedicalHistory (если у него другой формат ключа)
                db.session.query(MedicalHistory).filter_by(
                    passportdetails=old_passport
                ).update({
                    'passportdetails': new_passport
                })

            # Обновляем поля донора
            for field, value in data.items():
                if field not in ['old_passportdata', 'old_institutioncode'] and hasattr(donor, field):
                    setattr(donor, field, value)

            db.session.commit()

        return jsonify({'message': 'Данные донора успешно обновлены'}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating donor: {str(e)}")
        return jsonify({'message': 'Ошибка при обновлении донора', 'error': str(e)}), 500



@donor.route('/donor/search/<int:passportdata>/<int:institutioncode>', methods=['GET'])
def search_id(passportdata, institutioncode):
    try:
        # Выбираем сырые данные
        donor_data = db.session.query(
            Donor,
            MedicalInstitution._nameofinstitution.hex().label('inst_name_hex')
        ).join(
            MedicalInstitution, Donor.institutioncode == MedicalInstitution.institutioncode
        ).filter(
            Donor.passportdata == passportdata,
            Donor.institutioncode == institutioncode
        ).first_or_404()

        donor = donor_data[0]
        raw_name = donor_data.inst_name_hex  # Получаем hex-строку напрямую

        # Расшифровка
        cipher = MagmaCipher()
        try:
            institution_name = cipher.decrypt(bytes.fromhex(raw_name), mode='ECB').decode('utf-8') if raw_name else 'Неизвестное учреждение'
        except Exception as e:
            current_app.logger.error(f"[Decryption error] search_id: {e}")
            institution_name = 'Ошибка расшифровки'

        donor_dict = donor.to_dict()
        donor_dict['institution_name'] = institution_name

        return jsonify(donor_dict), 200
    except NotFound:
        return jsonify({'message': 'Donor not found.'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500

@donor.route('/donor/search')
def donor_search():
    query = request.args.get('q')

    donors = Donor.query.filter(
        (Donor._name.ilike(f'%{query}%')) |
        (Donor._secondname.ilike(f'%{query}%')) |
        (db.cast(Donor.passportdata, db.String).ilike(f'%{query}%'))
    ).limit(10).all()

    cipher = MagmaCipher()

    return jsonify({
        'donors': [{
            'passportData': donor.passportdata,
            'institutionCode': donor.institutioncode,
            'name': (cipher.decrypt(bytes.fromhex(donor._name), mode='ECB').decode('utf-8')
                     if donor._name else 'Неизвестно'),
            'secondName': (cipher.decrypt(bytes.fromhex(donor._secondname), mode='ECB').decode('utf-8')
                           if donor._secondname else 'Неизвестно'),
            'bloodGroup': (cipher.decrypt(bytes.fromhex(donor._bloodgroup), mode='ECB').decode('utf-8')
                           if donor._bloodgroup else None),
            'rhFactor': (cipher.decrypt(bytes.fromhex(donor._rhfactor), mode='ECB').decode('utf-8')
                         if donor._rhfactor else None)
        } for donor in donors]
    })