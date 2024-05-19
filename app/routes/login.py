from flask import Blueprint, render_template

login = Blueprint('login', __name__)


@login.route('/login')
def index():
    return render_template('main/login.html')


# @login.route('/login/examination', methods=['GET'])
# def examination():
#     return render_template('main/login.html')
