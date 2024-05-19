from ..extensions import db


class BloodCollection(db.Model):
    __tablename__ = 'bloodcollections'
    id = db.Column(db.Integer, primary_key=True)
    collection_date = db.Column(db.Date, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    collection_type = db.Column(db.String(50), nullable=False)
