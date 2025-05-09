from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db


class Donor(db.Model):
    __tablename__ = 'donor'

    passportdata = db.Column(db.Integer, primary_key=True)
    institutioncode = db.Column(db.Integer, db.ForeignKey('medicalinstitution.institutioncode'), primary_key=True)
    historynumber = db.Column(db.Integer, db.ForeignKey('medicalhistory.historynumber'))

    # ---------- ENCRYPTED FIELDS ----------

    _name = db.Column('name', db.String(100), nullable=False)
    _secondname = db.Column('secondname', db.String(100), nullable=False)
    _surname = db.Column('surname', db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    _gender = db.Column('gender', db.String(10), nullable=False)
    _address = db.Column('address', db.String(255), nullable=False)
    _phonenumber = db.Column('phonenumber', db.String(15), nullable=False)
    _polis = db.Column('polis', db.String(20), nullable=False)
    _bloodgroup = db.Column('bloodgroup', db.String(3), nullable=False)
    _rhfactor = db.Column('rhfactor', db.String(1), nullable=False)

    # ---------- ENCRYPTION METHODS ----------

    @hybrid_property
    def name(self):
        if self._name is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._name), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.name: {e}")
        return self._name

    @name.setter
    def name(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._name = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.name: {e}")
        else:
            self._name = value

    @hybrid_property
    def secondname(self):
        if self._secondname is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._secondname), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.secondname: {e}")
        return self._secondname

    @secondname.setter
    def secondname(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._secondname = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.secondname: {e}")
        else:
            self._secondname = value

    @hybrid_property
    def surname(self):
        if self._surname is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._surname), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.surname: {e}")
        return self._surname

    @surname.setter
    def surname(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._surname = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.surname: {e}")
        else:
            self._surname = value

    @hybrid_property
    def gender(self):
        if self._gender is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._gender), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.gender: {e}")
        return self._gender

    @gender.setter
    def gender(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._gender = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.gender: {e}")
        else:
            self._gender = value

    @hybrid_property
    def address(self):
        if self._address is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._address), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.address: {e}")
        return self._address

    @address.setter
    def address(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._address = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.address: {e}")
        else:
            self._address = value

    @hybrid_property
    def phonenumber(self):
        if self._phonenumber is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._phonenumber), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.phonenumber: {e}")
        return self._phonenumber

    @phonenumber.setter
    def phonenumber(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._phonenumber = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.phonenumber: {e}")
        else:
            self._phonenumber = value

    @hybrid_property
    def polis(self):
        if self._polis is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._polis), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.polis: {e}")
        return self._polis

    @polis.setter
    def polis(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._polis = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.polis: {e}")
        else:
            self._polis = value

    @hybrid_property
    def bloodgroup(self):
        if self._bloodgroup is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._bloodgroup), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] Donor.bloodgroup: {e}")
        return self._bloodgroup

    @bloodgroup.setter
    def bloodgroup(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._bloodgroup = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.bloodgroup: {e}")
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
                current_app.logger.error(f"[Decryption error] Donor.rhfactor: {e}")
        return self._rhfactor

    @rhfactor.setter
    def rhfactor(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._rhfactor = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] Donor.rhfactor: {e}")
        else:
            self._rhfactor = value

    def to_dict(self):
        return {
            'passportdata': self.passportdata,
            'institutioncode': self.institutioncode,
            'historynumber': self.historynumber,
            'name': self.name,
            'secondname': self.secondname,
            'surname': self.surname,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'gender': self.gender,
            'address': self.address,
            'phonenumber': self.phonenumber,
            'polis': self.polis,
            'bloodgroup': self.bloodgroup,
            'rhfactor': self.rhfactor,
        }
