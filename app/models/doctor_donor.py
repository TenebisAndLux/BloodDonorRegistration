from ..extensions import db
class DoctorDonor(db.Model):
    __tablename__ = 'doctordonor'
    passportdata = db.Column(db.Integer, primary_key=True)
    institutioncode = db.Column(db.Integer, primary_key=True)
    donationregistrationcode = db.Column(db.Integer, primary_key=True)
    servicenumber = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['passportdata', 'institutioncode'],
            ['donor.passportdata', 'donor.institutioncode']
        ),
        db.ForeignKeyConstraint(
            ['donationregistrationcode', 'servicenumber'],
            ['doctor.institutioncode', 'doctor.servicenumber']
        ),
    )