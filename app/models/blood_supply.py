from ..extensions import db

class BloodSupply(db.Model):
    __tablename__ = 'bloodsupply'
    collectiontypecode = db.Column(db.Integer, db.ForeignKey('bloodcollectiontype.collectiontypecode'), primary_key=True)
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    numberstock = db.Column(db.Integer, primary_key=True)
    numbercollections = db.Column(db.Integer)
    bloodgroup = db.Column(db.String(3))
    rhfactor = db.Column(db.String(1))
    bloodvolume = db.Column(db.Float)
    procurementdate = db.Column(db.Date)
    bestbeforedate = db.Column(db.Date)
    medicalinstitutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'))

    collections = db.relationship('BloodCollection', back_populates='bloodsupply',
                                  primaryjoin="and_(BloodSupply.collectiontypecode==BloodCollection.bloodsupplycollectiontypecode, "
                                              "BloodSupply.institutioncode==BloodCollection.bloodbankinstitutioncode, "
                                              "BloodSupply.numberstock==BloodCollection.numberstock)")