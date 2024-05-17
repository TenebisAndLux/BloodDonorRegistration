from flask import redirect, render_template, current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from config import host, user, password, port, db_name

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Сбросить пароль')


@current_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')

    login_form = LoginForm()
    forgot_password_form = ForgotPasswordForm()

    if login_form.validate_on_submit():
        user = Doctors.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect('/index')
        else:
            login_form.password.errors.append('Неверный пароль или логин')

    return render_template('login.html', login_form=login_form, forgot_password_form=forgot_password_form)


@current_app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect('/index')

    forgot_password_form = ForgotPasswordForm()

    if forgot_password_form.validate_on_submit():
        user = Doctors.query.filter_by(username=forgot_password_form.username.data,
                                       email=forgot_password_form.email.data).first()
        if user:
            # send password reset email
            return redirect('/login')
        else:
            forgot_password_form.username.errors.append('Неверный логин или email')

    return render_template('forgot_password.html', forgot_password_form=forgot_password_form)


@current_app.route('/index')
@login_required
def index():
    return render_template('index.html')


@current_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


login_manager = LoginManager(current_app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Doctors.query.get(int(user_id))


@current_app.context_processor
def inject_user():
    return {'user': current_user}

