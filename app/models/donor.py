from ..extensions import db


class Donor(db.Model):
    __tablename__ = 'donors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    hospital_affiliation = db.Column(db.String(255))
    passport_data = db.Column(db.String(50))
    insurance_data = db.Column(db.String(50))
    blood_type = db.Column(db.String(5), nullable=False)
    rh_factor = db.Column(db.String(5), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'address': self.address,
            'phone_number': self.phone_number,
            'hospital_affiliation': self.hospital_affiliation,
            'passport_data': self.passport_data,
            'insurance_data': self.insurance_data,
            'blood_type': self.blood_type,
            'rh_factor': self.rh_factor,
        }
