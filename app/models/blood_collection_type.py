from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from ..extensions import db


class BloodCollectionType(db.Model):
    __tablename__ = 'bloodcollectiontype'

    collectiontypecode = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name', db.String(100), nullable=False)

    @hybrid_property
    def name(self):
        if self._name is None:
            return None
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            try:
                return cipher.decrypt(bytes.fromhex(self._name), mode='ECB').decode('utf-8')
            except Exception as e:
                current_app.logger.error(f"[Decryption error] BloodCollectionType.name: {e}")
        return self._name  # fallback в случае ошибки

    @name.setter
    def name(self, value):
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if value and cipher:
            try:
                self._name = cipher.encrypt(value.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] BloodCollectionType.name: {e}")
        else:
            self._name = value