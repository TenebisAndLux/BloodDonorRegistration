from flask import Blueprint, render_template
from flask_login import login_required

information_system = Blueprint('information_system', __name__)


@information_system.route('/donor/list')
@login_required
def index():
    return render_template('main/index.html')
