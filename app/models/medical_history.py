from ..extensions import db


class MedicalHistory(db.Model):
    __tablename__ = 'medicalhistory'
    historynumber = db.Column(db.Integer, primary_key=True)
    passportdetails = db.Column(db.Integer, nullable=False)
    dateoflastexamination = db.Column(db.Date, nullable=False)
    analysisresults = db.Column(db.Text)
    banondonation = db.Column(db.Boolean, default=False)
