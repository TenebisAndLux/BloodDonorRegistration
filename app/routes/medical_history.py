import sys

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from .. import Doctor
from ..extensions import db
from ..models.blood_collection import BloodCollection
from ..models.medical_examination import MedicalExamination
from ..models.medical_history import MedicalHistory
from ..models.donor import Donor

medical_history = Blueprint('medical_history', __name__)

# Функция для очистки строк от неподдерживаемых символов
def clean_string(s):
    if isinstance(s, str):
        return s.encode('utf-8', errors='replace').decode('utf-8')
    return s

@medical_history.route('/donor/history')
def donor_history():
    passport = request.args.get('passport')
    institution = request.args.get('institution')

    # Получаем данные MedicalHistory
    medical_history = MedicalHistory.query.filter_by(passportdetails=passport).first()
    if not medical_history:
        medical_history = {
            'historynumber': None,
            'passportdetails': passport,
            'dateoflastexamination': None,
            'analysisresults': '',
            'banondonation': False
        }
    else:
        medical_history = {
            'historynumber': medical_history.historynumber,
            'passportdetails': medical_history.passportdetails,
            'dateoflastexamination': medical_history.dateoflastexamination.isoformat() if medical_history.dateoflastexamination else None,
            'analysisresults': clean_string(medical_history.analysisresults),
            'banondonation': medical_history.banondonation
        }

    # Получаем историю сборов крови
    collections = BloodCollection.query.filter_by(
        passportdata=passport,
        institutioncode=institution
    ).join(MedicalExamination, (MedicalExamination.passportdata == BloodCollection.passportdata) &
           (MedicalExamination.dateofexamination == BloodCollection.collectiondate)).join(
        Doctor, Doctor.servicenumber == BloodCollection.servicenumber
    ).all()

    blood_collections = []
    for collection in collections:
        exam = MedicalExamination.query.filter_by(
            passportdata=collection.passportdata,
            dateofexamination=collection.collectiondate
        ).first()
        doctor = Doctor.query.filter_by(servicenumber=collection.servicenumber).first()
        blood_collections.append({
            'id': {
                'bloodsupplycollectiontypecode': collection.bloodsupplycollectiontypecode,
                'bloodbankinstitutioncode': collection.bloodbankinstitutioncode,
                'numberstock': collection.numberstock,
                'number': collection.number
            },
            'date': collection.collectiondate.isoformat(),
            'type': {
                1: 'Цельная кровь',
                2: 'Плазма',
                3: 'Тромбоциты'
            }.get(collection.collectiontypecode, 'Неизвестно'),
            'volume': collection.bloodsupply.bloodvolume if collection.bloodsupply else 0,
            'doctor': f"{doctor.name} {doctor.secondname}" if doctor else 'Неизвестно',
            'notes': clean_string(exam.surveyresults) if exam else ''
        })

    return jsonify({
        'medicalHistory': medical_history,
        'bloodCollections': blood_collections
    })


@medical_history.route('/donor/history/update', methods=['POST'])
def update_donor_history():
    data = request.json
    try:
        medical_history = MedicalHistory.query.filter_by(historynumber=data['historynumber']).first()
        if medical_history:
            medical_history.analysisresults = data['analysisresults']
            medical_history.banondonation = data['banondonation']

        for collection in data['bloodCollections']:
            collection_id = collection['id']
            if not isinstance(collection_id, dict):
                print(f"Invalid collection id format: {collection_id}")
                raise ValueError(
                    "Collection id must be an object with bloodsupplycollectiontypecode, bloodbankinstitutioncode, numberstock, number")

            blood_collection = BloodCollection.query.get((
                collection_id['bloodsupplycollectiontypecode'],
                collection_id['bloodbankinstitutioncode'],
                collection_id['numberstock'],
                collection_id['number']
            ))
            if blood_collection:
                exam = MedicalExamination.query.filter_by(
                    passportdata=medical_history.passportdetails,
                    dateofexamination=blood_collection.collectiondate
                ).first()
                if exam:
                    exam.surveyresults = collection['notes']

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error 500'}), 500

@medical_history.route('/medical_history/get', methods=['GET'])
def get_medical_history():
    try:
        medical_histories = db.session.query(MedicalHistory, Donor).join(
            Donor, Donor.historynumber == MedicalHistory.historynumber).all()

        medical_history_list = []
        for history, donor in medical_histories:
            medical_history_dict = {
                'passportdata': donor.passportdata,
                'institutioncode': donor.institutioncode,
                'historynumber': donor.historynumber,
                'dateoflastexamination': history.dateoflastexamination.strftime('%Y-%m-%d') if history.dateoflastexamination else None,
                'analysisresults': history.analysisresults,
                'banondonation': history.banondonation,
                'name': donor.name,
                'secondname': donor.secondname,
                'surname': donor.surname,
                'polis': donor.polis,
            }
            medical_history_list.append(medical_history_dict)
        return jsonify(medical_history_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@medical_history.route('/medical_history/create', methods=['POST'])
def create_medical_history():
    try:
        data = request.get_json()
        dateoflastexamination = data['dateoflastexamination']
        analysisresults = data.get('analysisresults')
        banondonation = data['banondonation']

        history = MedicalHistory(
            dateoflastexamination=dateoflastexamination,
            analysisresults=analysisresults,
            banondonation=banondonation
        )

        db.session.add(history)
        db.session.commit()
        return jsonify({'success': 'Medical history created successfully', 'historynumber': history.historynumber})

    except KeyError as e:
        return jsonify({'error': f'Missing key in request: {e}'}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 400

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'exception': str(e)}), 500