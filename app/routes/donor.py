from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.donor import Donor

donor = Blueprint('donor', __name__)


@donor.route('/donor/<name>')
def create_donor(name):
    donor = Donor(name=name)
    db.session.add(donor)
    db.session.commit()
    return 'Donor be added'
