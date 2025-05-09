from flask_login import current_user

from ..extensions import db
from ..models.blood_collection import BloodCollection
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from ..models.blood_supply import BloodSupply
from ..models.donor import Donor
from ..models.medical_examination import MedicalExamination

from sqlalchemy import func

from ..models.medical_history import MedicalHistory

blood_collection = Blueprint('blood_collection', __name__)


@blood_collection.route('/blood_collection/create', methods=['POST'])
def create_blood_collection():
    data = request.json

    try:
        collectiondate = datetime.fromisoformat(data['date'])
        numberstock = int(collectiondate.strftime('%d%m%Y'))  # Например, 9052025 для 2025-05-09

        # Находим донора
        donor = Donor.query.filter_by(passportdata=data['donorPassport'], institutioncode=data['institutionCode']).first()
        if not donor:
            return jsonify({'error': 'Донор не найден'}), 404

        # Проверяем запрет на сдачу крови
        medical_history = MedicalHistory.query.filter_by(passportdetails=donor.passportdata).first()
        if medical_history and medical_history.banondonation:
            new_exam = MedicalExamination(
                passportdata=donor.passportdata,
                institutioncode=donor.institutioncode,
                surveyresults=data['notes'],
                dateofexamination=collectiondate,
                servicenumber=current_user.servicenumber
            )
            db.session.add(new_exam)
            db.session.commit()
            return jsonify({'error': 'У донора запрет на сдачу крови. Запись в MedicalExamination создана.'}), 403

        # Определяем группу крови и резус-фактор
        blood_group = data.get('bloodGroup', donor.bloodgroup)
        rh_factor = data.get('rhFactor', donor.rhfactor)

        # Проверяем или создаем запись в BloodSupply
        existing_supply = BloodSupply.query.filter_by(
            collectiontypecode=int(data['type']),
            institutioncode=int(data['institutionCode']),
            numberstock=numberstock,
            bloodgroup=blood_group,
            rhfactor=rh_factor
        ).first()

        if existing_supply:
            # Обновляем существующую запись
            existing_supply.numbercollections += 1
            existing_supply.bloodvolume += int(data['volume'])
        else:
            # Создаем новую запись
            new_supply = BloodSupply(
                collectiontypecode=int(data['type']),
                institutioncode=int(data['institutionCode']),
                numberstock=numberstock,
                numbercollections=1,
                bloodgroup=blood_group,
                rhfactor=rh_factor,
                bloodvolume=int(data['volume']),
                procurementdate=collectiondate,
                bestbeforedate=collectiondate + timedelta(days=90),  # Срок годности 90 дней
                medicalinstitutioncode=current_user.institutioncode
            )
            db.session.add(new_supply)

        # Сохраняем изменения в BloodSupply
        db.session.flush()

        # Создаем запись в BloodCollection
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

        # Создаем запись в MedicalExamination
        new_exam = MedicalExamination(
            passportdata=donor.passportdata,
            institutioncode=donor.institutioncode,
            surveyresults=data['notes'],
            dateofexamination=collectiondate,
            servicenumber=current_user.servicenumber
        )
        db.session.add(new_exam)

        # Фиксируем изменения
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500