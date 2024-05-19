from flask import Blueprint, render_template

index = Blueprint('index', __name__)


@index.route('/donor/list')
def index():
    return render_template('main/index.html')
