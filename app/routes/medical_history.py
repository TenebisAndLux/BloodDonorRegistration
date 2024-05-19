from ..extensions import db

class MedicalHistory(db.Model):
    __tablename__ = 'MedicalHistory'
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('Donors.id'), nullable=False)
    last_examination_date = db.Column(db.Date, nullable=False)
    test_results = db.Column(db.String(255))
    donation_ban = db.Column(db.Boolean, nullable=False)
