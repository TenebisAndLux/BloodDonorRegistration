from datetime import datetime
from operator import or_

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required

from .. import MagmaCipher
from ..extensions import db
from ..models import MedicalInstitution
from ..models.donor import Donor

donor_list = Blueprint('donor_list', __name__)

@donor_list.route('/donor_list/get', methods=['GET'])
@login_required
def get_donors():
    try:
        order = request.args.get('order', 'asc')
        donors = Donor.query.order_by(
            Donor.passportdata.asc() if order == 'asc' else Donor.passportdata.desc()
        ).all()

        donorsList = []
        for donor in donors:

            institution_name = donor.institution.nameofinstitution if donor.institution else "Неизвестное учреждение"
            donorDict = {
                'institutionname': institution_name,
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

@donor_list.route('/donor/list/search', methods=['GET'])
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

    query = db.session.query(Donor, MedicalInstitution).outerjoin(
        MedicalInstitution, Donor.institutioncode == MedicalInstitution.institutioncode
    )
    cipher = current_app.config.get('ENCRYPTION_CIPHER')

    if name:
        query = query.filter(Donor._name.ilike(f'%{name}%'))  # Используем _name вместо name
    if secondname:
        query = query.filter(Donor._secondname.ilike(f'%{secondname}%'))
    if surname:
        query = query.filter(Donor._surname.ilike(f'%{surname}%'))
    if address:
        query = query.filter(Donor._address.ilike(f'%{address}%'))
    if phonenumber:
        query = query.filter(Donor._phonenumber.ilike(f'%{phonenumber}%'))
    if polis:
        query = query.filter(Donor._polis.ilike(f'%{polis}%'))
    if birthday:
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        query = query.filter(Donor.birthday == birthday)
    if bloodgroup:
        query = query.filter(Donor._bloodgroup.ilike(f'%{bloodgroup}%'))
    if rhfactor:
        query = query.filter(Donor._rhfactor.ilike(f'%{rhfactor}%'))
    if gender:
        try:
            encrypted_gender = cipher.encrypt(gender.encode('utf-8'), mode='ECB').hex()
            query = query.filter(Donor._gender == encrypted_gender)
        except Exception as e:
            current_app.logger.error(f"[Encryption error] Gender search: {e}")
            return jsonify({'message': 'Search error'}), 500

    results = query.all()

    if not results:
        return jsonify({'message': 'Donors not found.'}), 404

    cipher = MagmaCipher()
    donors_list = []

    for donor_model, institution_model in results:
        donor_dict = donor_model.to_dict()
        institution_name = 'Неизвестное учреждение'

        if institution_model and institution_model._nameofinstitution:
            try:
                decrypted = cipher.decrypt(bytes.fromhex(institution_model._nameofinstitution), mode='ECB')
                institution_name = decrypted.decode('utf-8')
            except Exception as e:
                print(f"[Decryption error] Institution name: {e}")
                institution_name = 'Ошибка расшифровки'

        donor_dict['institutionname'] = institution_name
        donors_list.append(donor_dict)

    return jsonify(donors_list), 200

@donor_list.route('/donor/list/get/last', methods=['GET'])
def get_last_donor_id():
    try:
        last_donor = Donor.query.order_by(Donor.passportdata.desc()).first()
        if last_donor:
            return jsonify({'lastId': last_donor.passportdata}), 200
        else:
            return jsonify({'message': 'No donors found.'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500