from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect

from ..extensions import db


class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctor'

    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    servicenumber = db.Column(db.Integer, primary_key=True)
    _role = db.Column('role', db.String, nullable=False)
    _name = db.Column('name', db.String(100), nullable=False)
    _secondname = db.Column('secondname', db.String(100), nullable=False)
    _jobtitle = db.Column('jobtitle', db.String(100), nullable=False)
    _login = db.Column('login', db.String(50), nullable=False, unique=True)
    password = db.Column('password', db.String(255), nullable=False)
    _email = db.Column('email', db.String(255), nullable=False)

    institution = db.relationship('MedicalInstitution', backref='doctors')

    def _decrypt_field(self, field_value):
        """Общий метод для расшифровки поля"""
        if field_value is None:
            return None

        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                # Проверяем, что значение является строкой перед fromhex
                if isinstance(field_value, str):
                    return cipher.decrypt(bytes.fromhex(field_value), mode='ECB').decode('utf-8')
                return field_value  # Если не строка, возвращаем как есть
            except Exception as e:
                current_app.logger.error(f"[Decryption error] {e}")
        return field_value

    def _encrypt_field(self, value):
        """Общий метод для шифрования поля"""
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                return cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] {e}")
        return value

    @hybrid_property
    def role(self):
        # Для случая, когда обращаемся к классу (не к экземпляру)
        if not inspect(self).persistent:
            return self._role

        return self._decrypt_field(self._role)

    @role.setter
    def role(self, value):
        self._role = self._encrypt_field(value)

    @hybrid_property
    def name(self):
        if not inspect(self).persistent:
            return self._name
        return self._decrypt_field(self._name)

    @name.setter
    def name(self, value):
        self._name = self._encrypt_field(value)

    @hybrid_property
    def secondname(self):
        if not inspect(self).persistent:
            return self._secondname
        return self._decrypt_field(self._secondname)

    @secondname.setter
    def secondname(self, value):
        self._secondname = self._encrypt_field(value)

    @hybrid_property
    def jobtitle(self):
        if not inspect(self).persistent:
            return self._jobtitle
        return self._decrypt_field(self._jobtitle)

    @jobtitle.setter
    def jobtitle(self, value):
        self._jobtitle = self._encrypt_field(value)

    @hybrid_property
    def login(self):
        if not inspect(self).persistent:
            return self._login
        return self._decrypt_field(self._login)

    @login.setter
    def login(self, value):
        self._login = self._encrypt_field(value)

    @hybrid_property
    def email(self):
        if not inspect(self).persistent:
            return self._email
        return self._decrypt_field(self._email)

    @email.setter
    def email(self, value):
        self._email = self._encrypt_field(value)

    # ---------- PASSWORD ----------

    def set_password(self, value):
        self.password = generate_password_hash(value)

    def check_password(self, password_check):
        return check_password_hash(self.password, password_check)

    # ---------- ID и сериализация ----------

    def get_id(self):
        return f"{self.institutioncode}|{self.servicenumber}"

    def to_dict(self):
        return {
            'institutioncode': self.institutioncode,
            'servicenumber': self.servicenumber,
            'name': self.name,
            'secondname': self.secondname,
            'jobtitle': self.jobtitle,
            'login': self.login,
            'email': self.email,
            'role': self.role,
        }