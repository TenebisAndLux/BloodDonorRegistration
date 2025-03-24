from flask import Blueprint, render_template

report_system = Blueprint('report_system', __name__)


@report_system.route('/report')
def index():
    return render_template('main/report_index.html')