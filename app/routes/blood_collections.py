from flask import Blueprint
from ..extensions import db
from ..models.blood_collection import BloodCollection

blood_collection = Blueprint('blood_collection', __name__)


@blood_collection.route('/donor/list/blood_collection')
def create_blood_collection():
    blood_collection = BloodCollection()
    db.session.add(blood_collection)
    db.session.commit()
    return 'blood_collection Created Susses'
