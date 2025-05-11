from flask import Blueprint, render_template

hospital_info = Blueprint('hospital_info', __name__)


@hospital_info.route('/medical_institution/list')
def index():
    return render_template('main/medical_institution_index.html')