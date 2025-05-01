from ..extensions import db
class BloodCollectionType(db.Model):
    __tablename__ = 'bloodcollectiontype'
    collectiontypecode = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)