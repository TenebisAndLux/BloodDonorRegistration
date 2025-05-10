from flask import Blueprint, render_template

blood_bank = Blueprint('blood_bank', __name__)


@blood_bank.route('/blood_bank')
def index():
    return render_template('main/blood_bank_index.html')