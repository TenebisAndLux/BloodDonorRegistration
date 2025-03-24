from flask import Blueprint, render_template

doctor_info = Blueprint('doctor_info', __name__)


@doctor_info.route('/doctor/list')
def index():
    return render_template('main/doctor_index.html')
