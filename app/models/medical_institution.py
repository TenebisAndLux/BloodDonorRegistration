from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from ..extensions import db


class MedicalInstitution(db.Model):
    __tablename__ = 'medicalinstitution'

    institutioncode = db.Column(db.Integer, primary_key=True)

    # Encrypted fields
    _nameofinstitution = db.Column('nameofinstitution', db.String(255), nullable=False)
    _address = db.Column('address', db.String(255), nullable=False)
    _contactphonenumber = db.Column('contactphonenumber', db.String(15), nullable=False)
    _email = db.Column('email', db.String(255), nullable=False)
    _typeofinstitution = db.Column('typeofinstitution', db.String(100), nullable=False)

    # ---------- ENCRYPTED FIELDS ----------

    @hybrid_property
    def nameofinstitution(self):
        if self._nameofinstitution is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._nameofinstitution), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalInstitution.nameofinstitution: {e}")
        return self._nameofinstitution

    @nameofinstitution.setter
    def nameofinstitution(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._nameofinstitution = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalInstitution.nameofinstitution: {e}")
        else:
            self._nameofinstitution = value

    @hybrid_property
    def address(self):
        if self._address is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._address), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalInstitution.address: {e}")
        return self._address

    @address.setter
    def address(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._address = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalInstitution.address: {e}")
        else:
            self._address = value

    @hybrid_property
    def contactphonenumber(self):
        if self._contactphonenumber is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._contactphonenumber), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalInstitution.contactphonenumber: {e}")
        return self._contactphonenumber

    @contactphonenumber.setter
    def contactphonenumber(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._contactphonenumber = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalInstitution.contactphonenumber: {e}")
        else:
            self._contactphonenumber = value

    @hybrid_property
    def email(self):
        if self._email is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._email), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalInstitution.email: {e}")
        return self._email

    @email.setter
    def email(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._email = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalInstitution.email: {e}")
        else:
            self._email = value

    @hybrid_property
    def typeofinstitution(self):
        if self._typeofinstitution is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._typeofinstitution), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] MedicalInstitution.typeofinstitution: {e}")
        return self._typeofinstitution

    @typeofinstitution.setter
    def typeofinstitution(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._typeofinstitution = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] MedicalInstitution.typeofinstitution: {e}")
        else:
            self._typeofinstitution = value