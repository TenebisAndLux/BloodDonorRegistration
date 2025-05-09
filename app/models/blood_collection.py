from ..extensions import db


class BloodCollection(db.Model):
    __tablename__ = 'bloodcollection'
    bloodsupplycollectiontypecode = db.Column(db.Integer, primary_key=True)
    bloodbankinstitutioncode = db.Column(db.Integer, primary_key=True)
    numberstock = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    donationregistrationcode = db.Column(db.Integer)
    servicenumber = db.Column(db.Integer)
    passportdata = db.Column(db.Integer)
    institutioncode = db.Column(db.Integer)
    collectiondate = db.Column(db.Date)
    passportdetails = db.Column(db.Integer)
    collectiontypecode = db.Column(db.Integer, db.ForeignKey('bloodcollectiontype.collectiontypecode'))

    bloodsupply = db.relationship('BloodSupply', back_populates='collections',
                                  primaryjoin="and_(BloodSupply.collectiontypecode==BloodCollection.bloodsupplycollectiontypecode, "
                                              "BloodSupply.institutioncode==BloodCollection.bloodbankinstitutioncode, "
                                              "BloodSupply.numberstock==BloodCollection.numberstock)")
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['donationregistrationcode', 'servicenumber'],
            ['doctor.institutioncode', 'doctor.servicenumber']
        ),
        db.ForeignKeyConstraint(
            ['passportdata', 'institutioncode'],
            ['donor.passportdata', 'donor.institutioncode']
        ),
        db.ForeignKeyConstraint(
            ['bloodsupplycollectiontypecode', 'bloodbankinstitutioncode', 'numberstock'],
            ['bloodsupply.collectiontypecode', 'bloodsupply.institutioncode', 'bloodsupply.numberstock']
        ),
    )