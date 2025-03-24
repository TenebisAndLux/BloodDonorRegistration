from flask import Blueprint, render_template

hospital_info = Blueprint('hospital_info', __name__)


@hospital_info.route('/hospital/list')
def index():
    return render_template('main/hospital_index.html')