from flask_mail import Mail, Message
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from app.extensions import mail


def init_mail(app):
    mail.init_app(app)


def send_password_email(doctor_email, password):
    try:
        subject = "Ваш пароль от системы Donor Mirror"
        body = f"""
        Здравствуйте!

        Ваш текущий пароль от системы Donor Mirror: {password}

        Рекомендуем изменить пароль после входа в систему.

        С уважением,
        Команда Donor Mirror
        """

        msg = Message(subject=subject,
                      recipients=[doctor_email],
                      body=body)

        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False