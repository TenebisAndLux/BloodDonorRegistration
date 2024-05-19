from flask import Blueprint
from ..extensions import db
from ..models.medical_history import MedicalHistory

medical_history = Blueprint('medical_history', __name__)


@medical_history.route('/donor/list/medical_history')
def create_medical_history():
    medical_history = MedicalHistory()
    db.session.add(medical_history)
    db.session.commit()
    return 'medical_history Created Susses'
