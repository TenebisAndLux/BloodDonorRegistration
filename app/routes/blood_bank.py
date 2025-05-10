from flask import Blueprint, render_template, request, jsonify, current_app
from ..models import BloodSupply, BloodCollectionType, MedicalInstitution, Doctor
from ..extensions import db
from datetime import datetime
from sqlalchemy import and_, func
import math
from flask_login import current_user, login_required

blood_bank = Blueprint('blood_bank', __name__)


@blood_bank.route('/blood_bank')
def index():
    return render_template('main/blood_bank_index.html')


def get_current_institution_code():
    """Получаем код учреждения текущего врача"""
    if not current_user.is_authenticated:
        return None

    try:
        # Получаем doctor_id из current_user
        doctor_id_parts = current_user.get_id().split('|')
        if len(doctor_id_parts) < 2:
            return None

        institution_code = int(doctor_id_parts[0])
        servicenumber = int(doctor_id_parts[1])

        # Проверяем существование врача
        doctor = Doctor.query.filter_by(
            institutioncode=institution_code,
            servicenumber=servicenumber
        ).first()

        return doctor.institutioncode if doctor else None

    except (ValueError, IndexError, AttributeError) as e:
        current_app.logger.error(f"Error getting institution code: {str(e)}")
        return None


@blood_bank.route('/blood_bank/search')
@login_required
def search_blood():
    try:
        institution_code = get_current_institution_code()
        if not institution_code:
            return jsonify({'error': 'Не удалось определить медицинское учреждение'}), 403

        cipher = current_app.config.get('ENCRYPTION_CIPHER')

        # Получаем и шифруем параметры поиска
        blood_group = request.args.get('blood_group', '').strip().upper()
        if blood_group and cipher:
            try:
                blood_group = cipher.encrypt(blood_group.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] blood_group: {e}")
                blood_group = ''  # Если не удалось зашифровать, ищем без фильтра

        rh_factor = request.args.get('rh_factor', '').strip()
        if rh_factor and cipher:
            try:
                rh_factor = cipher.encrypt(rh_factor.encode('utf-8'), mode='ECB').hex()
            except Exception as e:
                current_app.logger.error(f"[Encryption error] rh_factor: {e}")
                rh_factor = ''

        best_before = request.args.get('best_before', '').strip()

        query = db.session.query(
            BloodSupply,
            BloodCollectionType._name.label('collection_type_raw')
        ).join(
            BloodCollectionType,
            BloodCollectionType.collectiontypecode == BloodSupply.collectiontypecode
        ).filter(
            BloodSupply.institutioncode == institution_code
        )

        if blood_group:
            query = query.filter(BloodSupply._bloodgroup == blood_group)
        if rh_factor:
            query = query.filter(BloodSupply._rhfactor == rh_factor)
        if best_before:
            try:
                date_obj = datetime.strptime(best_before, '%Y-%m-%d').date()
                query = query.filter(BloodSupply.bestbeforedate >= date_obj)
            except ValueError:
                current_app.logger.warning(f"Invalid date format: {best_before}")

        supplies = []
        for supply, collection_type_raw in query.all():
            # Расшифровываем тип заготовки
            collection_type = None
            if collection_type_raw and cipher:
                try:
                    collection_type = cipher.decrypt(bytes.fromhex(collection_type_raw), mode='ECB').decode('utf-8')
                except Exception as e:
                    current_app.logger.error(f"[Decryption error] BloodCollectionType.name: {e}")
                    collection_type = collection_type_raw

            supplies.append({
                'collectiontypecode': supply.collectiontypecode,
                'institutioncode': supply.institutioncode,
                'numberstock': supply.numberstock,
                'blood_group': supply.bloodgroup,
                'rh_factor': supply.rhfactor,
                'blood_volume': supply.bloodvolume,
                'procurement_date': supply.procurementdate.strftime('%Y-%m-%d') if supply.procurementdate else None,
                'best_before_date': supply.bestbeforedate.strftime('%Y-%m-%d') if supply.bestbeforedate else None,
                'collection_type': collection_type
            })

        return jsonify(supplies)

    except Exception as e:
        current_app.logger.error(f"Error in blood bank search: {str(e)}", exc_info=True)
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


@blood_bank.route('/blood_bank/write_off', methods=['POST'])
def write_off():
    try:
        data = request.get_json()
        institution_code = get_current_institution_code()
        if not institution_code:
            return jsonify({'error': 'Не удалось определить медицинское учреждение'}), 400

        # Проверяем, что запись принадлежит текущему учреждению
        if data['institutioncode'] != institution_code:
            return jsonify({'error': 'Нельзя списать запись другого учреждения'}), 403

        # Удаляем запись в bloodsupply
        db.session.execute(
            "DELETE FROM bloodsupply WHERE "
            "collectiontypecode = :ctc AND "
            "institutioncode = :ic AND "
            "numberstock = :ns",
            {
                'ctc': data['collectiontypecode'],
                'ic': data['institutioncode'],
                'ns': data['numberstock']
            }
        )

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error writing off blood supply: {str(e)}")
        return jsonify({'error': str(e)}), 500


@blood_bank.route('/blood_bank/request', methods=['POST'])
def request_blood():
    try:
        data = request.get_json()
        blood_group = data['blood_group'].upper()
        rh_factor = data['rh_factor']

        institution_code = get_current_institution_code()
        if not institution_code:
            return jsonify({'error': 'Не удалось определить медицинское учреждение'}), 400

        # Получаем текущее учреждение
        current_institution = MedicalInstitution.query.get(institution_code)
        if not current_institution:
            return jsonify({'error': 'Ваше медицинское учреждение не найдено'}), 400

        # Шифруем параметры поиска
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        try:
            encrypted_blood_group = cipher.encrypt(blood_group.encode('utf-8'), mode='ECB').hex()
            encrypted_rh_factor = cipher.encrypt(rh_factor.encode('utf-8'), mode='ECB').hex()
        except Exception as e:
            current_app.logger.error(f"Encryption error: {e}")
            return jsonify({'error': 'Ошибка обработки параметров поиска'}), 500

        # Ищем кровь в других больницах
        query = db.session.query(
            BloodSupply,
            MedicalInstitution
        ).join(
            MedicalInstitution,
            MedicalInstitution.institutioncode == BloodSupply.institutioncode
        ).filter(
            BloodSupply._bloodgroup == encrypted_blood_group,
            BloodSupply._rhfactor == encrypted_rh_factor,
            BloodSupply.institutioncode != institution_code,
            BloodSupply.bestbeforedate >= datetime.now().date()
        )

        hospitals = []
        for supply, institution in query.all():
            try:
                # Расшифровываем данные больницы
                hospital_name = institution.nameofinstitution
                hospital_address = institution.address

                hospitals.append({
                    'name': hospital_name,
                    'address': hospital_address,
                    'blood_volume': supply.bloodvolume
                })
            except Exception as e:
                current_app.logger.error(f"Error processing hospital data: {e}")
                continue

        if not hospitals:
            return jsonify({'error': 'Кровь не найдена в других больницах'}), 404

        # Добавляем адрес текущего учреждения
        return jsonify({
            'hospitals': hospitals,
            'current_hospital_address': current_institution.address
        })

    except Exception as e:
        current_app.logger.error(f"Error in blood request: {str(e)}")
        return jsonify({'error': str(e)}), 500


def calculate_distance(lat1, lon1, lat2, lon2):
    # Формула гаверсинусов для расчета расстояния между точками
    R = 6371  # Радиус Земли в км
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c