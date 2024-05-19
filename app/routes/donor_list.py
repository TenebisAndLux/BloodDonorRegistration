from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..extensions import db
from ..models.donor import Donor

donor_list = Blueprint('donor_list', __name__)


@donor_list.route('/donor/list/get', methods=['GET'])
def get():
    donors = Donor.query.all()
    return donors
