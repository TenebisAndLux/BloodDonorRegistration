from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.blood_collection import BloodCollection

blood_collection = Blueprint('blood_collection', __name__)


@blood_collection.route('/blood_collection/<record>')
def create_donor(record):
    blood_collection = BloodCollection(record=record)
    db.session.add(blood_collection)
    db.session.commit()
    return 'BloodCollection be added'
