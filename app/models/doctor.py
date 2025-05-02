from ..extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Doctor(db.Model, UserMixin):
    __tablename__ = 'doctor'
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    servicenumber = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    secondname = db.Column(db.String(100), nullable=False)
    jobtitle = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    institution = db.relationship('MedicalInstitution', backref='doctors')

    def get_id(self):
        return f"{self.institutioncode}|{self.servicenumber}"

    def set_password(self, password_set):
        self.password = generate_password_hash(password_set)

    def check_password(self, password_check):
        return check_password_hash(self.password, password_check)

    def to_dict(self):
        return {
            'institutioncode': self.institutioncode,
            'servicenumber': self.servicenumber,
            'name': self.name,
            'secondname': self.secondname,
            'jobtitle': self.jobtitle,
            'login': self.login,
            'email': self.email,
        }
    