from urllib import request

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user

from ..extensions import db
from ..models.report import Report

report = Blueprint('report', __name__)


@report.route('/report/<record>')
def create_donor(record):
    report = Report(record=record)
    db.session.add(report)
    db.session.commit()
    return 'Report be added'
