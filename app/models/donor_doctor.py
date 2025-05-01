from ..extensions import db

class DonorDoctor(db.Model):
    __tablename__ = 'donordonor'
    donationregistrationcode = db.Column(db.Integer, primary_key=True)
    servicenumber = db.Column(db.Integer, primary_key=True)
    passportdata = db.Column(db.Integer, primary_key=True)
    institutioncode = db.Column(db.Integer, primary_key=True)

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
