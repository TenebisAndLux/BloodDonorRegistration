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
