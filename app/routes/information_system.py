from flask import Blueprint, render_template

information_system = Blueprint('information_system', __name__)


@information_system.route('/donor/list')
def index():
    return render_template('main/index.html')
