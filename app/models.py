from .extensions import db


class Donors(db.Model):
    __tablename__ = 'Donors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    hospital_affiliation = db.Column(db.String(100))
    passport_data = db.Column(db.String(20))
    insurance_data = db.Column(db.String(20))
    blood_type = db.Column(db.String(5), nullable=False)
    rh_factor = db.Column(db.String(5), nullable=False)


class MedicalHistory(db.Model):
    __tablename__ = 'MedicalHistory'
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('Donors.id'), nullable=False)
    last_examination_date = db.Column(db.Date, nullable=False)
    test_results = db.Column(db.String(255))
    donation_ban = db.Column(db.Boolean, nullable=False)


class BloodCollections(db.Model):
    __tablename__ = 'BloodCollections'
    id = db.Column(db.Integer, primary_key=True)
    collection_date = db.Column(db.Date, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('Donors.id'), nullable=False)
    collection_type = db.Column(db.String(50), nullable=False)


class Reports(db.Model):
    __tablename__ = 'Reports'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    report_content = db.Column(db.Text)
    report_file = db.Column(db.LargeBinary)


class Doctors(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
