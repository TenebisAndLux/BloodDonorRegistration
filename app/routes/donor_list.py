from flask import Blueprint, render_template

donor_list = Blueprint('donor_list', __name__)


@donor_list.route('/donor/list')
def index():
    return render_template('main/index.html')
