from ..extensions import db

class BloodCollections(db.Model):
    __tablename__ = 'BloodCollections'
    id = db.Column(db.Integer, primary_key=True)
    collection_date = db.Column(db.Date, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('Donors.id'), nullable=False)
    collection_type = db.Column(db.String(50), nullable=False)