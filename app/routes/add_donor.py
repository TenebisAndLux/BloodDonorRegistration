from datetime import datetime
from aiohttp import web

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from werkzeug.exceptions import NotFound

from ..extensions import db
from ..models.donor import Donor

donor = Blueprint('donor', __name__)


@donor.route('/donor/add', methods=['POST'])
def create():
    data = request.get_json()
    donor = Donor(
        first_name=data.get('addDonorFirstName'),
        last_name=data.get('addDonorLastName'),
        middle_name=data.get('addDonorMiddleName'),
        date_of_birth=data.get('addDonorDateOfBirth'),
        gender=data.get('addDonorGender'),
        address=data.get('addDonorAddress'),
        phone_number=data.get('addDonorPhoneNumber'),
        hospital_affiliation=data.get('addDonorHospitalAffiliation'),
        passport_data=data.get('addDonorPassportData'),
        insurance_data=data.get('addDonorInsuranceData'),
        blood_type=data.get('addDonorBloodType'),
        rh_factor=data.get('addDonorRhFactor')
    )
    db.session.add(donor)
    db.session.commit()
    return jsonify({'message': 'Donor created successfully.', 'id': donor.id})


@donor.route('/donor/edit/<int:donor_id>', methods=['POST'])
def edit(donor_id):
    donor = Donor.query.get(donor_id)
    if donor:
        data = request.get_json()
        for field in donor.to_dict():
            if field in data:
                setattr(donor, field, data[field])
        db.session.commit()
        return jsonify({'message': 'Donor updated successfully.'})
    return jsonify({'message': 'Donor not found.'}), 404


@donor.route('/donor/search/<int:id>', methods=['GET'])
def search_id(id):
    try:
        donor = Donor.query.get_or_404(id)
        return jsonify(donor.to_dict())
    except NotFound:
        return jsonify({'message': 'Donor not found.'}), 404
    except Exception:
        return jsonify({'message': 'An error occurred.'}), 500
    

@donor.route('/donor/list/search', methods=['GET'])
def search_donors():
    last_name = request.args.get('last_name')
    middle_name = request.args.get('middle_name')
    first_name = request.args.get('first_name')
    hospital_affiliation = request.args.get('hospital_affiliation')
    address = request.args.get('address')
    phone_number = request.args.get('phone_number')
    insurance_data = request.args.get('insurance_data')
    date_of_birth = request.args.get('date_of_birth')
    blood_type = request.args.get('blood_type')
    rh_factor = request.args.get('rh_factor')

    query = Donor.query
    if last_name:
        query = query.filter(Donor.last_name.ilike(f'%{last_name}%'))
    if middle_name:
        query = query.filter(Donor.middle_name.ilike(f'%{middle_name}%'))
    if first_name:
        query = query.filter(Donor.first_name.ilike(f'%{first_name}%'))
    if hospital_affiliation:
        query = query.filter(Donor.hospital_affiliation.ilike(f'%{hospital_affiliation}%'))
    if address:
        query = query.filter(Donor.address.ilike(f'%{address}%'))
    if phone_number:
        query = query.filter(Donor.phone_number.ilike(f'%{phone_number}%'))
    if insurance_data:
        query = query.filter(Donor.insurance_data.ilike(f'%{insurance_data}%'))
    if date_of_birth:
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        query = query.filter(Donor.date_of_birth == date_of_birth)
    if blood_type:
        query = query.filter(Donor.blood_type.ilike(f'%{blood_type}%'))
    if rh_factor:
        query = query.filter(Donor.rh_factor.ilike(f'%{rh_factor}%'))

    donors = query.all()

    if not donors:
        return jsonify({'message': 'Donors not found.'}), 404

    donors_list = []
    for donor in donors:
        donor_dict = donor.to_dict()
        donor_dict['date_of_birth'] = donor.date_of_birth.strftime('%Y-%m-%d')
        donors_list.append(donor_dict)

    return jsonify(donors_list)


@donor.route('/donor/list/get/last', methods=['GET'])
def get_last_donor_id():
    try:
        last_donor = Donor.query.order_by(Donor.id.desc()).first()
        if last_donor:
            return jsonify({'last_id': last_donor.id})
        else:
            return jsonify({'message': 'No donors found.'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500