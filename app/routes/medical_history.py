from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.medical_history import MedicalHistory
from ..models.donor import Donor

medical_history = Blueprint('medical_history', __name__)


@medical_history.route('/medical_history/get', methods=['GET'])
def get():
    try:
        medical_histories = db.session.query(MedicalHistory, Donor).join(
            Donor, Donor.id == MedicalHistory.donor_id).all()
        medical_history_list = []
        for medical_history, donor in medical_histories:
            medical_history_dict = {
                'donor_id': donor.id,
                'last_examination_date': medical_history.last_examination_date.strftime('%Y-%m-%d'),
                'test_results': medical_history.test_results,
                'donation_ban': medical_history.donation_ban,
                'hospital_affiliation': donor.hospital_affiliation,
                'first_name': donor.first_name,
                'last_name': donor.last_name,
                'insurance_data': donor.insurance_data,
            }
            medical_history_list.append(medical_history_dict)
        return jsonify(medical_history_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@medical_history.route('/medical_history/create', methods=['POST'])
def create_medical_history():
    try:
        donor_id = request.json['donor_id']
        last_examination_date = request.json['last_examination_date']
        test_results = request.json['test_results']
        donation_ban = request.json['donation_ban']

        medical_history = MedicalHistory(donor_id=donor_id,
                                         last_examination_date=last_examination_date,
                                         test_results=test_results,
                                         donation_ban=donation_ban)
        db.session.add(medical_history)
        db.session.commit()
        return jsonify({'success': 'Medical History created successfully'})
    
    except KeyError as e:
        return jsonify({'error': 'Отсутствует обязательный ключ в запросе'}), 400
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Ошибка с целостностью данных в БД'}), 400
        
    except Exception as e:
        return jsonify({'error': 'Внутренняя ошибка сервера', 'exception': str(e)}), 500