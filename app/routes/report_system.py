import io
from flask import Blueprint, render_template, request, send_file, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from docx import Document
from datetime import datetime, timedelta
from app import db
from app.models import Donor, Doctor, MedicalInstitution, MedicalExamination, MedicalHistory, BloodSupply, \
    BloodCollectionType, BloodCollection

report_system = Blueprint('report_system', __name__)

def prepare_donor_report_data(blood_collection):
    """Подготовка данных для отчета о доноре"""
    donor = Donor.query.filter_by(passportdata=blood_collection.passportdata).first_or_404(
        description="Донор не найден")

    doctor = Doctor.query.filter_by(servicenumber=blood_collection.servicenumber).first_or_404(
        description="Врач не найден")

    institution = MedicalInstitution.query.get_or_404(
        blood_collection.institutioncode,
        description="Учреждение не найдено")

    medical_examination = MedicalExamination.query.filter(
        MedicalExamination.passportdata == donor.passportdata,
        MedicalExamination.dateofexamination <= blood_collection.collectiondate
    ).order_by(MedicalExamination.dateofexamination.desc()).first()

    medical_history = MedicalHistory.query.get_or_404(
        donor.historynumber,
        description="Медицинская история не найдена")

    blood_supply = BloodSupply.query.filter_by(
        numberstock=blood_collection.numberstock).first()

    collection_type = BloodCollectionType.query.get_or_404(
        blood_collection.collectiontypecode,
        description="Тип сбора крови не найден")

    return {
        'donor': donor,
        'doctor': doctor,
        'institution': institution,
        'medical_examination': medical_examination,
        'medical_history': medical_history,
        'blood_supply': blood_supply,
        'collection_type': collection_type,
        'blood_collection': blood_collection
    }


@report_system.route('/reports/generate_report_1', methods=['POST'])
def generate_report_1():
    """Генерация отчета о доноре с предпросмотром"""
    try:
        # Валидация данных
        required_fields = ['collectiontypecode', 'institutioncode', 'numberstock', 'number']
        if not all(field in request.form for field in required_fields):
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400

        collectiontypecode = int(request.form['collectiontypecode'])
        institutioncode = int(request.form['institutioncode'])
        numberstock = int(request.form['numberstock'])
        number = int(request.form['number'])

        # Получаем данные
        blood_collection = BloodCollection.query.filter_by(
            bloodsupplycollectiontypecode=collectiontypecode,
            bloodbankinstitutioncode=institutioncode,
            numberstock=numberstock,
            number=number
        ).first_or_404(description="Событие сбора крови не найдено")

        report_data = prepare_donor_report_data(blood_collection)

        # Если запрос на предпросмотр
        if request.form.get('preview') == 'true':
            preview_content = {
                'donor_name': f"{report_data['donor'].surname} {report_data['donor'].name}",
                'institution': report_data['institution'].nameofinstitution,
                'collection_date': blood_collection.collectiondate.strftime("%d.%m.%Y"),
                'blood_volume': report_data['blood_supply'].bloodvolume if report_data['blood_supply'] else "N/A"
            }
            return jsonify(preview_content)

        # Генерация DOCX
        doc = generate_donor_docx(report_data)

        # Отправка файла
        return send_docx_response(doc, f"donor_report_{blood_collection.collectiondate.strftime('%Y%m%d')}.docx")

    except ValueError as e:
        return jsonify({'error': f"Некорректные данные: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': f"Ошибка сервера: {str(e)}"}), 500


def generate_donor_docx(report_data):
    """Генерация DOCX файла для отчета о доноре"""
    doc = Document()
    # [Остальная логика генерации документа...]
    return doc


def send_docx_response(doc, filename):
    """Отправка DOCX файла в ответе"""
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    response = make_response(file_stream.getvalue())
    response.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response


@report_system.route('/reports/generate_report_2', methods=['POST'])
def generate_report_2():
    """Генерация сводного отчета по учреждению с предпросмотром"""
    try:
        # Валидация данных
        required_fields = ['institutioncode', 'start_date', 'end_date']
        if not all(field in request.form for field in required_fields):
            return jsonify({'error': 'Не все обязательные поля заполнены'}), 400

        institutioncode = int(request.form['institutioncode'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

        if start_date > end_date:
            return jsonify({'error': 'Дата начала не может быть позже даты окончания'}), 400

        institution = MedicalInstitution.query.get_or_404(
            institutioncode, description="Учреждение не найдено")

        # Если запрос на предпросмотр
        if request.form.get('preview') == 'true':
            # Простая статистика для предпросмотра
            total_donors = db.session.query(db.func.count(db.distinct(BloodCollection.passportdata))).filter(
                BloodCollection.institutioncode == institutioncode,
                BloodCollection.collectiondate.between(start_date, end_date)
            ).scalar()

            return jsonify({
                'institution': institution.nameofinstitution,
                'period': f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}",
                'total_donors': total_donors
            })

        # Генерация полного отчета
        doc = generate_institution_docx(institutioncode, start_date, end_date)
        return send_docx_response(doc, f"institution_report_{institutioncode}_{datetime.now().strftime('%Y%m%d')}.docx")

    except ValueError as e:
        return jsonify({'error': f"Некорректные данные: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': f"Ошибка сервера: {str(e)}"}), 500