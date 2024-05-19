from flask import Blueprint
from ..extensions import db
from ..models.report import Report

report = Blueprint('report', __name__)


@report.route('/donor/list/report')
def create_report():
    report = Report()
    db.session.add(report)
    db.session.commit()
    return 'report Created Susses'
