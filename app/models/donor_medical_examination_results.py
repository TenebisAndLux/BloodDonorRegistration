from ..extensions import db

class DonorMedicalExaminationResults(db.Model):
    __tablename__ = 'donormedicalexaminationresults'
    number = db.Column(db.Integer, db.ForeignKey('medicalexamination.number'), primary_key=True)
    passportdata = db.Column(db.Integer, primary_key=True)
    institutioncode = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['passportdata', 'institutioncode'],
            ['donor.passportdata', 'donor.institutioncode']
        ),
    )
