from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.medical_history import MedicalHistory

medical_history = Blueprint('medical_history', __name__)


@medical_history.route('/medical_history/<record>')
def create_donor(record):
    medical_history = MedicalHistory(record=record)
    db.session.add(medical_history)
    db.session.commit()
    return 'MedicalHistory be added'
