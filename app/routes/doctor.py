from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.doctor import Doctor

doctor = Blueprint('doctor', __name__)


@doctor.route('/doctor/<name>')
def create_donor(name):
    doctor = Doctor(name=name)
    db.session.add(doctor)
    db.session.commit()
    return 'Doctor be added'


@doctor.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form
        doctor = Doctor.query.filter_by(login=login_data['login']).first()
        if doctor and doctor.password == login_data['password']:
            login_user(doctor)
            return redirect(url_for('doctor.index'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html')
