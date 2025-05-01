from ..extensions import db


class Doctor(db.Model):
    __tablename__ = 'doctor'
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    servicenumber = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    secondname = db.Column(db.String(100), nullable=False)
    jobtitle = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

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
    