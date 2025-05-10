from flask_login import current_user

from ..extensions import db
from ..models.blood_collection import BloodCollection
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

from ..models.blood_supply import BloodSupply
from ..models.donor import Donor
from ..models.medical_examination import MedicalExamination

from sqlalchemy import func
from app.crypto.magma_cipher import MagmaCipher
from ..models.medical_history import MedicalHistory

blood_collection = Blueprint('blood_collection', __name__)


@blood_collection.route('/blood_collection/create', methods=['POST'])
def create_blood_collection():
    data = request.json
    cipher = current_app.config.get('ENCRYPTION_CIPHER')

    try:
        collectiondate = datetime.fromisoformat(data['date'])
        numberstock = int(collectiondate.strftime('%d%m%Y'))

        # Находим донора
        donor = Donor.query.filter_by(
            passportdata=data['donorPassport'],
            institutioncode=data['institutionCode']
        ).first()
        if not donor:
            return jsonify({'error': 'Донор не найден'}), 404

        # Расшифровка ФИО донора
        try:
            name_to_decrypt = donor._name if isinstance(donor._name, str) else donor._name.hex()
            donor_name = cipher.decrypt(bytes.fromhex(name_to_decrypt), mode='ECB').decode('utf-8') if donor._name else 'Неизвестно'
        except Exception as e:
            current_app.logger.error(f"[Decryption error] Donor.name: {e}")
            donor_name = 'Ошибка расшифровки'

        try:
            secondname_to_decrypt = donor._secondname if isinstance(donor._secondname, str) else donor._secondname.hex()
            donor_secondname = cipher.decrypt(bytes.fromhex(secondname_to_decrypt), mode='ECB').decode('utf-8') if donor._secondname else 'Неизвестно'
        except Exception as e:
            current_app.logger.error(f"[Decryption error] Donor.secondname: {e}")
            donor_secondname = 'Ошибка расшифровки'

        # Используем зашифрованные значения группы крови и резус-фактора от донора
        blood_group = donor._bloodgroup
        rh_factor = donor._rhfactor

        # Проверяем или создаём запись в BloodSupply
        existing_supply = BloodSupply.query.filter_by(
            collectiontypecode=int(data['type']),
            institutioncode=int(data['institutionCode']),
            numberstock=numberstock,
            _bloodgroup=blood_group,
            _rhfactor=rh_factor
        ).first()

        if existing_supply:
            existing_supply.numbercollections += 1
            existing_supply.bloodvolume += int(data['volume'])
        else:
            new_supply = BloodSupply(
                collectiontypecode=int(data['type']),
                institutioncode=int(data['institutionCode']),
                numberstock=numberstock,
                numbercollections=1,
                _bloodgroup=blood_group,
                _rhfactor=rh_factor,
                bloodvolume=int(data['volume']),
                procurementdate=collectiondate,
                bestbeforedate=collectiondate + timedelta(days=90),
                medicalinstitutioncode=current_user.institutioncode
            )
            db.session.add(new_supply)

        db.session.flush()

        # Получаем уникальный номер для MedicalExamination
        last_exam_number = db.session.query(db.func.max(MedicalExamination.number)).scalar()
        new_exam_number = (last_exam_number or 0) + 1

        # Проверяем запрет на сдачу крови
        medical_history = MedicalHistory.query.filter_by(passportdetails=donor.passportdata).first()
        if medical_history and medical_history.banondonation:
            new_exam = MedicalExamination(
                number=new_exam_number,
                passportdata=donor.passportdata,
                institutioncode=donor.institutioncode,
                _surveyresults=cipher.encrypt(data['notes'].encode('utf-8'), mode='ECB').hex() if data.get(
                    'notes') else None,
                dateofexamination=collectiondate,
                servicenumber=current_user.servicenumber
            )
            db.session.add(new_exam)
            db.session.commit()

            return jsonify({
                'error': 'У донора запрет на сдачу крови. Запись в MedicalExamination создана.',
                'donorName': donor_name,
                'donorSecondName': donor_secondname
            }), 403

        # Создаём запись в BloodCollection
        last_number = db.session.query(db.func.max(BloodCollection.number)).filter(
            BloodCollection.collectiondate == collectiondate,
            BloodCollection.institutioncode == data['institutionCode']
        ).scalar()
        new_number = (last_number or 0) + 1

        new_collection = BloodCollection(
            bloodsupplycollectiontypecode=int(data['type']),
            bloodbankinstitutioncode=int(data['institutionCode']),
            numberstock=numberstock,
            number=new_number,
            passportdata=donor.passportdata,
            institutioncode=donor.institutioncode,
            collectiondate=collectiondate,
            servicenumber=current_user.servicenumber,
            collectiontypecode=int(data['type'])
        )
        db.session.add(new_collection)

        # Создаём запись в MedicalExamination
        new_exam = MedicalExamination(
            number=new_exam_number,
            passportdata=donor.passportdata,
            institutioncode=donor.institutioncode,
            _surveyresults=cipher.encrypt(data['notes'].encode('utf-8'), mode='ECB').hex() if data.get(
                'notes') else None,
            dateofexamination=collectiondate,
            servicenumber=current_user.servicenumber
        )
        db.session.add(new_exam)

        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500