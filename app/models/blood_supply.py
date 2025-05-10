from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db


class BloodSupply(db.Model):
    __tablename__ = 'bloodsupply'

    collectiontypecode = db.Column(db.Integer, db.ForeignKey('bloodcollectiontype.collectiontypecode'),
                                   primary_key=True)
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    numberstock = db.Column(db.Integer, primary_key=True)
    numbercollections = db.Column(db.Integer)
    _bloodgroup = db.Column('bloodgroup', db.String(3))
    _rhfactor = db.Column('rhfactor', db.String(1))
    bloodvolume = db.Column(db.Float)
    procurementdate = db.Column(db.Date)
    bestbeforedate = db.Column(db.Date)
    medicalinstitutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'))

    collections = db.relationship('BloodCollection', back_populates='bloodsupply',
                                  primaryjoin="and_("
                                              "BloodSupply.collectiontypecode==BloodCollection.bloodsupplycollectiontypecode, "
                                              "BloodSupply.institutioncode==BloodCollection.bloodbankinstitutioncode, "
                                              "BloodSupply.numberstock==BloodCollection.numberstock)")

    @hybrid_property
    def bloodgroup(self):
        if self._bloodgroup is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._bloodgroup), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] BloodSupply.bloodgroup: {e}")
        return self._bloodgroup

    @bloodgroup.setter
    def bloodgroup(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._bloodgroup = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] BloodSupply.bloodgroup: {e}")
        else:
            self._bloodgroup = value

    @hybrid_property
    def rhfactor(self):
        if self._rhfactor is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._rhfactor), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] BloodSupply.rhfactor: {e}")
        return self._rhfactor

    @rhfactor.setter
    def rhfactor(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._rhfactor = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] BloodSupply.rhfactor: {e}")
        else:
            self._rhfactor = value
