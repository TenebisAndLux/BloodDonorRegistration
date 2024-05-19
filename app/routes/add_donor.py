from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..extensions import db
from ..models.donor import Donor

donor = Blueprint('donor', __name__)


@donor.route('/donor/add', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        donor = Donor(
            first_name=request.form['addDonorFirstName'],
            last_name=request.form['addDonorLastName'],
            middle_name=request.form['addDonorMiddleName'],
            date_of_birth=request.form['addDonorDateOfBirth'],
            gender=request.form['addDonorGender'],
            address=request.form['addDonorAddress'],
            phone_number=request.form['addDonorPhoneNumber'],
            hospital_affiliation=request.form['addDonorHospitalAffiliation'],
            passport_data=request.form['addDonorPassportData'],
            insurance_data=request.form['addDonorInsuranceData'],
            blood_type=request.form['addDonorBloodType'],
            rh_factor=request.form['addDonorRhFactor']
        )
        db.session.add(donor)
        db.session.commit()
        flash('Donor created successfully.')
        return redirect(url_for('donor.add', donor_id=donor.id))
    else:
        return render_template('main/index.html')


@donor.route('/donor/edit/<int:donor_id>', methods=['GET', 'POST'])
def edit(donor_id):
    donor = Donor.query.get(donor_id)
    if donor and request.method == 'POST':
        donor.first_name = request.form.get('editDonorFirstName')
        donor.last_name = request.form.get('editDonorLastName')
        donor.middle_name = request.form.get('editDonorMiddleName')
        donor.date_of_birth = request.form.get('editDonorDateOfBirth')
        donor.gender = request.form.get('editDonorGender')
        donor.address = request.form.get('editDonorAddress')
        donor.phone_number = request.form.get('editDonorPhoneNumber')
        donor.hospital_affiliation = request.form.get('editDonorHospitalAffiliation')
        donor.passport_data = request.form.get('editDonorPassportData')
        donor.insurance_data = request.form.get('editDonorInsuranceData')
        donor.blood_type = request.form.get('editDonorBloodType')
        donor.rh_factor = request.form.get('editDonorRhFactor')
        db.session.commit()
        flash('Donor updated successfully.')
    return redirect(url_for('donor.add', donor_id=donor_id))


@donor.route('/donor/search/<int:donor_id>', methods=['GET'])
def search(donor_id):
    donor = Donor.query.get(donor_id)
    return donor
