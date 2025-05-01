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
    surveyresults = db.Column(db.Text)
    personnelnumber = db.Column(db.Integer)

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
