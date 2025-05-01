from ..extensions import db


class Donor(db.Model):
    __tablename__ = 'donor'
    passportdata = db.Column(db.Integer, primary_key=True)
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    historynumber = db.Column(db.Integer, db.ForeignKey('medicalhistory.historynumber'))
    name = db.Column(db.String(100), nullable=False)
    secondname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    polis = db.Column(db.String(20), nullable=False)
    bloodgroup = db.Column(db.String(3), nullable=False)
    rhfactor = db.Column(db.String(1), nullable=False)

    def to_dict(self):
        return {
            'passportdata': self.passportdata,
            'institutioncode': self.institutioncode,
            'historynumber': self.historynumber,
            'name': self.name,
            'secondname': self.secondname,
            'surname': self.surname,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'gender': self.gender,
            'address': self.address,
            'phonenumber': self.phonenumber,
            'polis': self.polis,
            'bloodgroup': self.bloodgroup,
            'rhfactor': self.rhfactor,
        }
