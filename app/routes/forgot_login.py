from flask import Blueprint, render_template

forgot_login = Blueprint('forgot_login', __name__)


@forgot_login.route('/login/forgot')
def index():
    return render_template('main/login_forgot.html')
