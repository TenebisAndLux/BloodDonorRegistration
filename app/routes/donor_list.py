from flask import Blueprint, jsonify, request
from flask_login import login_required

from ..extensions import db
from ..models.donor import Donor

donor_list = Blueprint('donor_list', __name__)

@donor_list.route('/donor_list/get', methods=['GET'])
@login_required
def get_donors():
    try:
        order = request.args.get('order', 'asc')
        # Сортировка по паспорту и institutioncode
        donors = Donor.query.order_by(
            Donor.passportdata.asc() if order == 'asc' else Donor.passportdata.desc()
        ).all()

        donorsList = []
        for donor in donors:
            donorDict = {
                'passportdata': donor.passportdata,
                'institutioncode': donor.institutioncode,
                'historynumber': donor.historynumber,
                'name': donor.name,
                'secondname': donor.secondname,
                'surname': donor.surname,
                'birthday': donor.birthday.strftime('%Y-%m-%d') if donor.birthday else None,
                'gender': donor.gender,
                'address': donor.address,
                'phonenumber': donor.phonenumber,
                'polis': donor.polis,
                'bloodgroup': donor.bloodgroup,
                'rhfactor': donor.rhfactor,
            }
            donorsList.append(donorDict)
        return jsonify(donorsList)
    except Exception as e:
        return jsonify({'error': str(e)}), 500