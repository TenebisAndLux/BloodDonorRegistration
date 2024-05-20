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
def search(id):
    try:
        donor = Donor.query.get_or_404(id)
        return jsonify(donor.to_dict())
    except NotFound:
        return jsonify({'message': 'Donor not found.'}), 404
    except Exception:
        return jsonify({'message': 'An error occurred.'}), 500
