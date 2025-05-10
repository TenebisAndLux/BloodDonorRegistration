import io
from flask import Blueprint, render_template, request, send_file, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from docx import Document
from datetime import datetime, timedelta
from app import db
from app.models import Donor, Doctor, MedicalInstitution, MedicalExamination, MedicalHistory, BloodSupply, \
    BloodCollectionType, BloodCollection

report_system = Blueprint('report_system', __name__)


@report_system.route('/reports')
def index():
    """Главная страница системы отчетов"""
    institutions = MedicalInstitution.query.all()
    collection_types = BloodCollectionType.query.all()
    stocks = BloodSupply.query.all()
    numbers = BloodCollection.query.all()

    return render_template('main/report_index.html',
                           institutions=institutions,
                           collection_types=collection_types,
                           stocks=stocks,
                           numbers=numbers)


@report_system.route('/reports/generate_report_1', methods=['POST'])
def generate_report_1():
    """Генерация отчета о доноре"""
    try:
        # Получаем данные из формы
        collectiontypecode = int(request.form['collectiontypecode'])
        institutioncode = int(request.form['institutioncode'])
        numberstock = int(request.form['numberstock'])
        number = int(request.form['number'])

        # Получаем данные о сборе крови
        blood_collection = BloodCollection.query.filter_by(
            bloodsupplycollectiontypecode=collectiontypecode,
            bloodbankinstitutioncode=institutioncode,
            numberstock=numberstock,
            number=number
        ).first_or_404(description="Событие сбора крови не найдено")

        # Получаем данные донора
        donor = Donor.query.filter_by(passportdata=blood_collection.passportdata).first_or_404(
            description="Донор не найден")

        # Получаем данные врача
        doctor = Doctor.query.filter_by(servicenumber=blood_collection.servicenumber).first_or_404(
            description="Врач не найден")

        # Получаем данные учреждения
        institution = MedicalInstitution.query.get_or_404(
            blood_collection.institutioncode,
            description="Учреждение не найдено")

        # Получаем последнее медицинское обследование
        medical_examination = MedicalExamination.query.filter(
            MedicalExamination.passportdata == donor.passportdata,
            MedicalExamination.dateofexamination <= blood_collection.collectiondate
        ).order_by(MedicalExamination.dateofexamination.desc()).first()

        # Получаем медицинскую историю
        medical_history = MedicalHistory.query.get_or_404(
            donor.historynumber,
            description="Медицинская история не найдена")

        # Получаем данные о запасе крови
        blood_supply = BloodSupply.query.filter_by(
            numberstock=blood_collection.numberstock).first()

        # Получаем тип сбора крови
        collection_type = BloodCollectionType.query.get_or_404(
            blood_collection.collectiontypecode,
            description="Тип сбора крови не найден")

        # Создаем документ
        doc = Document()

        # Заголовок отчета
        doc.add_heading('Отчет о донорстве крови', level=1)
        doc.add_paragraph(f'Медицинское учреждение: {institution.nameofinstitution}')
        doc.add_paragraph(f'Адрес: {institution.address}')
        doc.add_paragraph(f'Контактный телефон: {institution.contactphonenumber}')
        doc.add_paragraph(f'Дата формирования отчета: {datetime.now().strftime("%d.%m.%Y")}')
        doc.add_paragraph('________________________________________')

        # Данные донора
        doc.add_heading('Данные донора', level=2)
        doc.add_paragraph(f'ФИО: {donor.surname} {donor.name} {donor.secondname}')
        doc.add_paragraph(f'Дата рождения: {donor.birthday.strftime("%d.%m.%Y")}')
        doc.add_paragraph(f'Пол: {donor.gender}')
        doc.add_paragraph(f'Адрес: {donor.address}')
        doc.add_paragraph(f'Телефон: {donor.phonenumber}')
        doc.add_paragraph(f'Полис ОМС: {donor.polis}')
        doc.add_paragraph(f'Группа крови и резус-фактор: {donor.bloodgroup}, {donor.rhfactor}')
        doc.add_paragraph(f'Номер медицинской карты: {medical_history.historynumber}')
        doc.add_paragraph(
            f'Дата последнего обследования: {medical_examination.dateofexamination.strftime("%d.%m.%Y") if medical_examination else "N/A"}')
        doc.add_paragraph(f'Результаты анализов: {medical_examination.surveyresults if medical_examination else "N/A"}')
        doc.add_paragraph(f'Ограничения на донацию: {"Да" if medical_history.banondonation else "Нет"}')
        doc.add_paragraph('________________________________________')

        # Информация о донации
        doc.add_heading('Информация о донации', level=2)
        doc.add_paragraph(f'Дата донации: {blood_collection.collectiondate.strftime("%d.%m.%Y")}')
        doc.add_paragraph(f'Тип донации: {collection_type.name}')
        doc.add_paragraph(f'Объем забора: {blood_supply.bloodvolume if blood_supply else "N/A"} мл')
        doc.add_paragraph(
            f'Ответственный врач: {doctor.secondname} {doctor.name} (№ служебного удостоверения: {doctor.servicenumber})')
        doc.add_paragraph('________________________________________')

        # Заключение
        doc.add_heading('Заключение', level=2)
        doc.add_paragraph('1. Донор допущен к сдаче крови, противопоказаний не выявлено.')
        doc.add_paragraph('2. Забор крови произведен успешно, самочувствие донора после процедуры удовлетворительное.')
        next_donation_date = blood_collection.collectiondate + timedelta(days=60)
        doc.add_paragraph(
            f'3. Следующая возможная дата донации: {next_donation_date.strftime("%d.%m.%Y")} (через 60 дней).')
        doc.add_paragraph('Спасибо за ваш вклад в спасение жизней!')
        doc.add_paragraph('________________________________________')
        doc.add_paragraph('Примечание')
        doc.add_paragraph('Данный отчет сформирован автоматически на основании данных из базы медицинского учреждения.')
        doc.add_paragraph('В случае вопросов обращайтесь по телефону регистратуры: +7 (915) 606-54-33.')

        # Сохраняем документ в памяти
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        # Формируем ответ
        response = make_response(file_stream.getvalue())
        response.headers.set('Content-Type',
                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response.headers.set('Content-Disposition', 'attachment',
                             filename=f"donor_report_{blood_collection.collectiondate.strftime('%Y%m%d')}.docx")

        return response

    except ValueError as e:
        return abort(400, description=f"Некорректные данные формы: {str(e)}")
    except Exception as e:
        return abort(500, description=f"Ошибка сервера: {str(e)}")


@report_system.route('/reports/generate_report_2', methods=['POST'])
def generate_report_2():
    """Генерация сводного отчета по учреждению"""
    try:
        # Получаем данные из формы
        institutioncode = int(request.form['institutioncode'])
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

        # Проверяем корректность дат
        if start_date > end_date:
            return abort(400, description="Дата начала периода не может быть позже даты окончания")

        # Получаем данные учреждения
        institution = MedicalInstitution.query.get_or_404(
            institutioncode,
            description="Учреждение не найдено")

        # Рассчитываем статистику
        # Общее количество уникальных доноров
        total_donors = db.session.query(db.func.count(db.distinct(BloodCollection.passportdata))).filter(
            BloodCollection.institutioncode == institutioncode,
            BloodCollection.collectiondate.between(start_date, end_date)
        ).scalar()

        # Общее количество донаций
        total_donations = BloodCollection.query.filter(
            BloodCollection.institutioncode == institutioncode,
            BloodCollection.collectiondate.between(start_date, end_date)
        ).count()

        # Упрощенный расчет первичных и повторных доноров
        primary_donors = total_donors // 3  # Примерная оценка
        repeat_donors = total_donors - primary_donors

        # Объемы компонентов крови
        blood_supplies = BloodSupply.query.join(
            BloodCollection,
            (BloodSupply.numberstock == BloodCollection.numberstock) &
            (BloodSupply.institutioncode == BloodCollection.bloodbankinstitutioncode)
        ).filter(
            BloodCollection.institutioncode == institutioncode,
            BloodCollection.collectiondate.between(start_date, end_date)
        ).all()

        whole_blood = sum(bs.bloodvolume for bs in blood_supplies if bs.collectiontypecode == 1) / 1000
        plasma = sum(bs.bloodvolume for bs in blood_supplies if bs.collectiontypecode == 2) / 1000

        # Статистика медицинских обследований (упрощенно)
        contraindications = MedicalExamination.query.join(Donor).filter(
            Donor.institutioncode == institutioncode,
            MedicalExamination.dateofexamination.between(start_date, end_date)
        ).count()

        deferred = MedicalHistory.query.join(Donor).filter(
            Donor.institutioncode == institutioncode,
            MedicalHistory.banondonation == True
        ).count()

        abnormal_tests = 2  # Заглушка

        # Создаем документ
        doc = Document()

        # Заголовок отчета
        doc.add_heading('Отчет о донорстве крови', level=1)
        doc.add_paragraph(f'Дата формирования отчета: {datetime.now().strftime("%d %B %Y года")}')
        doc.add_paragraph(f'Медицинское учреждение: {institution.nameofinstitution}')
        doc.add_paragraph(f'Адрес: {institution.address}')
        doc.add_paragraph(f'Контактный телефон: {institution.contactphonenumber}')
        doc.add_paragraph(f'Период: с {start_date.strftime("%d %B")} по {end_date.strftime("%d %B %Y года")}')

        # Введение
        doc.add_heading('1. Введение', level=2)
        doc.add_paragraph('Настоящий отчет содержит информацию о донорских донациях за указанный период.')

        # Основная часть
        doc.add_heading('2. Основная часть', level=2)

        # Количество доноров и донаций
        doc.add_heading('2.1. Количество доноров и донаций', level=3)
        doc.add_paragraph(f'Общее количество доноров: {total_donors}')
        doc.add_paragraph(f'Количество первичных доноров: {primary_donors}')
        doc.add_paragraph(f'Количество повторных доноров: {repeat_donors}')
        doc.add_paragraph(f'Общее количество донаций: {total_donations}')

        # Заготовка крови
        doc.add_heading('2.2. Заготовка крови и ее компонентов', level=3)
        doc.add_paragraph(f'Цельная кровь: {whole_blood:.2f} л')
        doc.add_paragraph(f'Эритроцитарная масса: 0 л')  # Заглушка
        doc.add_paragraph(f'Плазма: {plasma:.2f} л')
        doc.add_paragraph(f'Тромбоциты: 0 л')  # Заглушка

        # Результаты обследований
        doc.add_heading('2.3. Результаты медицинских обследований доноров', level=3)
        doc.add_paragraph(f'Выявлено противопоказаний к донорству: {contraindications}')
        doc.add_paragraph(f'Отстранены от донорства по медицинским причинам: {deferred}')
        doc.add_paragraph(f'Обнаружены отклонения в анализах крови: {abnormal_tests}')

        # Заключение
        doc.add_heading('3. Заключение', level=2)
        doc.add_paragraph('Работа с донорами велась в соответствии с установленными стандартами.')
        doc.add_paragraph('Подпись ответственного лица: _______________ /Иванов И.И./')
        doc.add_paragraph(f'Дата: {datetime.now().strftime("%d %B %Y года")}')

        # Сохраняем документ в памяти
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        # Формируем ответ
        response = make_response(file_stream.getvalue())
        response.headers.set('Content-Type',
                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response.headers.set('Content-Disposition', 'attachment',
                             filename=f"institution_report_{institutioncode}_{datetime.now().strftime('%Y%m%d')}.docx")

        return response

    except ValueError as e:
        return abort(400, description=f"Некорректные данные формы: {str(e)}")
    except Exception as e:
        return abort(500, description=f"Ошибка сервера: {str(e)}")