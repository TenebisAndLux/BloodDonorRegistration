from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_login import current_user
from werkzeug.exceptions import NotFound
from sqlalchemy import cast, String

from .. import Doctor
from ..extensions import db
from ..models import MedicalInstitution
from ..models.blood_collection import BloodCollection
from ..models.blood_collection_type import BloodCollectionType
from ..models.blood_supply import BloodSupply
from ..models.donor import Donor
from ..models.medical_examination import MedicalExamination

donor = Blueprint('donor', __name__)

@donor.route('/donor/add', methods=['POST'])
def create():
    data = request.get_json()

    donor = Donor(
        passportdata=data.get('passportdata'),
        institutioncode=data.get('institutioncode'),
        historynumber=data.get('historynumber'),
        name=data.get('name'),
        secondname=data.get('secondname'),
        surname=data.get('surname'),
        birthday=data.get('birthday'),
        gender=data.get('gender'),
        address=data.get('address'),
        phonenumber=data.get('phonenumber'),
        polis=data.get('polis'),
        bloodgroup=data.get('bloodgroup'),
        rhfactor=data.get('rhfactor')
    )

    try:
        db.session.add(donor)
        db.session.commit()
        return jsonify({'message': 'Донор успешно создан. ', 'id': donor.passportdata}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Данный донор есть в системе.'}), 500


@donor.route('/donor/edit/<int:passportdata>/<int:institutioncode>', methods=['POST'])
def edit(passportdata, institutioncode):
    donor = Donor.query.get_or_404((passportdata, institutioncode))
    data = request.get_json()

    for field in donor.to_dict():
        if field in data:
            setattr(donor, field, data[field])

    try:
        db.session.commit()
        return jsonify({'message': 'Donor updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during donor update.', 'error': str(e)}), 500


@donor.route('/donor/search/<int:passportdata>/<int:institutioncode>', methods=['GET'])
def search_id(passportdata, institutioncode):
    try:
        donor_data = db.session.query(Donor, MedicalInstitution.nameofinstitution).join(
            MedicalInstitution, Donor.institutioncode == MedicalInstitution.institutioncode
        ).filter(Donor.passportdata == passportdata, Donor.institutioncode == institutioncode).first_or_404()

        donors = donor_data[0]
        institution_name = donor_data[1] if donor_data[1] else 'Неизвестное учреждение'

        donor_dict = donors.to_dict()
        donor_dict['institution_name'] = institution_name

        return jsonify(donor_dict), 200
    except NotFound:
        return jsonify({'message': 'Donor not found.'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500

@donor.route('/donor/search')
def donor_search():
    query = request.args.get('q')

    donors = Donor.query.filter(
        (Donor.name.ilike(f'%{query}%')) |
        (Donor.secondname.ilike(f'%{query}%')) |
        (cast(Donor.passportdata, String).ilike(f'%{query}%'))
    ).limit(10).all()

    return jsonify({
        'donors': [{
            'passportData': donor.passportdata,
            'institutionCode': donor.institutioncode,
            'name': donor.name,
            'secondName': donor.secondname,
            'bloodGroup': donor.bloodgroup,
            'rhFactor': donor.rhfactor
        } for donor in donors]
    })

@donor.route('/donor/list/search', methods=['GET'])
def search_donors():
    name = request.args.get('name')
    secondname = request.args.get('secondname')
    surname = request.args.get('surname')
    birthday = request.args.get('birthday')
    gender = request.args.get('gender')
    address = request.args.get('address')
    phonenumber = request.args.get('phonenumber')
    polis = request.args.get('polis')
    bloodgroup = request.args.get('bloodgroup')
    rhfactor = request.args.get('rhfactor')

    query = db.session.query(Donor, MedicalInstitution.nameofinstitution).outerjoin(
        MedicalInstitution, Donor.institutioncode == MedicalInstitution.institutioncode
    )

    if name:
        query = query.filter(Donor.name.ilike(f'%{name}%'))
    if secondname:
        query = query.filter(Donor.secondname.ilike(f'%{secondname}%'))
    if surname:
        query = query.filter(Donor.surname.ilike(f'%{surname}%'))
    if address:
        query = query.filter(Donor.address.ilike(f'%{address}%'))
    if phonenumber:
        query = query.filter(Donor.phonenumber.ilike(f'%{phonenumber}%'))
    if polis:
        query = query.filter(Donor.polis.ilike(f'%{polis}%'))
    if birthday:
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        query = query.filter(Donor.birthday == birthday)
    if bloodgroup:
        query = query.filter(Donor.bloodgroup.ilike(f'%{bloodgroup}%'))
    if rhfactor:
        query = query.filter(Donor.rhfactor.ilike(f'%{rhfactor}%'))
    if gender:
        query = query.filter(Donor.gender.ilike(f'%{gender}%'))

    results = query.all()

    if not results:
        return jsonify({'message': 'Donors not found.'}), 404

    donors_list = []
    for donor, nameofinstitution in results:
        donor_dict = donor.to_dict()
        donor_dict['institutionname'] = nameofinstitution if nameofinstitution else 'Неизвестное учреждение'
        donors_list.append(donor_dict)

    return jsonify(donors_list), 200

@donor.route('/donor/list/get/last', methods=['GET'])
def get_last_donor_id():
    try:
        last_donor = Donor.query.order_by(Donor.passportdata.desc()).first()
        if last_donor:
            return jsonify({'lastId': last_donor.passportdata}), 200
        else:
            return jsonify({'message': 'No donors found.'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500