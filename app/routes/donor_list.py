from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from ..extensions import db
from ..models.donor import Donor

donor_list = Blueprint('donor_list', __name__)


@donor_list.route('/donor/list/get', methods=['GET'])
def get():
    try:
        order = request.args.get('order', 'asc')
        donors = Donor.query.order_by(Donor.id.asc() if order == 'asc' else Donor.id.desc()).all()
        donors_list = []
        for donor in donors:
            donor_dict = {
                'id': donor.id,
                'first_name': donor.first_name,
                'last_name': donor.last_name,
                'middle_name': donor.middle_name,
                'date_of_birth': donor.date_of_birth.strftime('%Y-%m-%d'),
                'gender': donor.gender,
                'address': donor.address,
                'phone_number': donor.phone_number,
                'hospital_affiliation': donor.hospital_affiliation,
                'passport_data': donor.passport_data,
                'insurance_data': donor.insurance_data,
                'blood_type': donor.blood_type,
                'rh_factor': donor.rh_factor
            }
            donors_list.append(donor_dict)
        return jsonify(donors_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
