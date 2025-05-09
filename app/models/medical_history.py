from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from ..extensions import db


class MedicalHistory(db.Model):
    __tablename__ = 'medicalhistory'

    historynumber = db.Column(db.Integer, primary_key=True)
    passportdetails = db.Column(db.Integer, nullable=False)
    dateoflastexamination = db.Column(db.Date, nullable=False)

    # Encrypted field
    _analysisresults = db.Column('analysisresults', db.Text)

    banondonation = db.Column(db.Boolean, default=False)

    # ---------- ENCRYPTED FIELDS ----------

    @hybrid_property
    def analysisresults(self):
        if self._analysisresults is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._analysisresults), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalHistory.analysisresults: {e}")
        return self._analysisresults

    @analysisresults.setter
    def analysisresults(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._analysisresults = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalHistory.analysisresults: {e}")
        else:
            self._analysisresults = value
