from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models.medical_history import MedicalHistory
from ..models.donor import Donor

medical_history = Blueprint('medical_history', __name__)

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