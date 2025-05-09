from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from ..extensions import db


class MedicalExamination(db.Model):
    __tablename__ = 'medicalexamination'

    number = db.Column(db.Integer, primary_key=True)
    passportdata = db.Column(db.Integer)
    institutioncode = db.Column(db.Integer)
    donationregistrationcode = db.Column(db.Integer)
    servicenumber = db.Column(db.Integer)
    passportdetails = db.Column(db.Integer)
    dateofexamination = db.Column(db.Date)

    # Encrypted field
    _surveyresults = db.Column('surveyresults', db.Text)

    personnelnumber = db.Column(db.Integer)

    # ---------- ENCRYPTED FIELDS ----------

    @hybrid_property
    def surveyresults(self):
        if self._surveyresults is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._surveyresults), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalExamination.surveyresults: {e}")
        return self._surveyresults

    @surveyresults.setter
    def surveyresults(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._surveyresults = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalExamination.surveyresults: {e}")
        else:
            self._surveyresults = value

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['donationregistrationcode', 'servicenumber'],
            ['doctor.institutioncode', 'doctor.servicenumber']
        ),
        db.ForeignKeyConstraint(
            ['passportdata', 'institutioncode'],
            ['donor.passportdata', 'donor.institutioncode']
        ),
    )
