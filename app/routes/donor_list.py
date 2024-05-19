from flask import Blueprint, render_template
from ..extensions import db
from ..models.donor import Donor

donor_list = Blueprint('donor_list', __name__)


@donor_list.route('/donor/list')
def index():
    return render_template('main/index.html')


# @donor_list.route('/donor/list')
# def create():
#     donor_list = Donor()
#     db.session.add(donor_list)
#     db.session.commit()
#     return 'Donor Create'