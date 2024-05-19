from flask import Blueprint, render_template, redirect, url_for, request, flash
from .extensions import db
from .models import Doctors, Donors, BloodCollections, MedicalHistory, Reports
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

doctor = Blueprint('doctor', __name__)

@doctor.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form
        doctor = Doctors.query.filter_by(login=login_data['login']).first()
        if doctor and doctor.password == login_data['password']:
            login_user(doctor)
            return redirect(url_for('doctor.index'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')

@doctor.route('/index')
@login_required
def index():
    donors = Donors.query.all()
    return render_template('index.html', donors=donors)

@doctor.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('doctor.login'))

@doctor.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        login_data = request.form
        doctor = Doctors.query.filter_by(login=login_data['login']).first()
        if doctor and doctor.email == login_data['email']:
            password = doctor.password
            send_email(doctor.email, password)
            flash('Пароль отправлен на указанный email')
        else:
            flash('Неверный логин или email')
    return render_template('forget_password.html')

def send_email(email, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    message = MIMEMultipart()
    message['From'] = 'your_email@gmail.com'
    message['To'] = email
    message['Subject'] = 'Ваш пароль'
    body = f'Ваш пароль: {password}'
    message.attach(MIMEText(body, 'plain'))
    server.send_message(message)
    server.quit()

@doctor.route('/donor/add', methods=['POST'])
@login_required
def add_donor():
    donor_data = request.form
    donor = Donors(
        first_name=donor_data['first_name'],
        last_name=donor_data['last_name'],
        date_of_birth=donor_data['date_of_birth'],
        gender=donor_data['gender'],
        blood_type=donor_data['blood_type'],
        rh_factor=donor_data['rh_factor']
    )
    db.session.add(donor)
    db.session.commit()
    flash('Донор добавлен')
    return redirect(url_for('doctor.index'))

@doctor.route('/donor/<int:donor_id>', methods=['GET', 'POST'])
@login_required
def donor_view(donor_id):
    donor = Donors.query.get_or_404(donor_id)
    if request.method == 'POST':
        if 'delete' in request.form:
            db.session.delete(donor)
            db.session.commit()
            flash('Донор удален')
            return redirect(url_for('doctor.index'))
        elif 'edit' in request.form:
            return redirect(url_for('doctor.edit_donor', donor_id=donor_id))
    return render_template('donor_view.html', donor=donor)

@doctor.route('/donor/<int:donor_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_donor(donor_id):
    donor = Donors.query.get_or_404(donor_id)
    if request.method == 'POST':
        donor_data = request.form
        donor.first_name = donor_data['first_name']
        donor.last_name = donor_data['last_name']
        donor.date_of_birth = donor_data['date_of_birth']
        donor.gender = donor_data['gender']
        donor.blood_type = donor_data['blood_type']
        donor.rh_factor = donor_data['rh_factor']
        db.session.commit()
        flash('Донор изменен')
        return redirect(url_for('doctor.donor_view', donor_id=donor_id))
    return render_template('edit_donor.html', donor=donor)

@doctor.route('/history')
@login_required
def history():
    reports = Reports.query.order_by(Reports.creation_date.desc()).all()
    return render_template('history.html', reports=reports)

@doctor.route('/add_report', methods=['GET', 'POST'])
@login_required
def add_report():
    if request.method == 'POST':
        report_data = request.form
        report = Reports(
            report_type=report_data['report_type'],
            creation_date=datetime.now(),
            report_content=report_data['report_content']
        )
        db.session.add(report)
        db.session.commit()
        flash('Отчет добавлен')
        return redirect(url_for('doctor.history'))
    return render_template('add_report.html')
