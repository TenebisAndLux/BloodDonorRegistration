from ..extensions import db

class MedicalInstitution(db.Model):
    __tablename__ = 'medicalinstitution'
    institutioncode = db.Column(db.Integer, primary_key=True)
    nameofinstitution = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contactphonenumber = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    typeofinstitution = db.Column(db.String(100), nullable=False)
