from ..extensions import db

class Report(db.Model):
    __tablename__ = 'Reports'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    report_content = db.Column(db.Text)
    report_file = db.Column(db.LargeBinary)