from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash

import app
from flask import current_app
from ..models.doctor import Doctor, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login_page():
    return render_template('main/login.html', csrf_token=generate_csrf())


@auth.route('/login', methods=['POST'])
def login():
    print("\n=== LOGIN REQUEST RECEIVED ===")

    try:
        # Log raw request data
        print("[1] Raw request data:", request.data.decode('utf-8'))

        data = request.get_json()
        if not data:
            print("[ERROR] No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        print("[2] Parsed JSON data:", data)

        login = data.get('login')
        password = data.get('password')
        print(f"[3] Attempting login for: {login}")

        # Шифруем логин, как это сделано в базе данных
        cipher = current_app.config.get('ENCRYPTION_CIPHER')
        if cipher:
            print(f"login: {login}")
            print(f"login.encode('utf-8'): {login.encode('utf-8')}")
            encrypted_login = cipher.encrypt(login.encode('utf-8'), mode='ECB').hex()
            print(f"encrypted_login: {cipher.encrypt(login.encode('utf-8'), mode='ECB').hex()}")
        else:
            encrypted_login = login  # Если шифратор не доступен, работаем с простым логином (не рекомендуется)

        # Database query for encrypted login
        doctor = Doctor.query.filter_by(_login=encrypted_login).first()
        if not doctor:
            print(f"[ERROR] Doctor not found for login: {login}")
            return jsonify({'error': 'Invalid credentials'}), 401

        print(f"[4] Doctor found - ID: {doctor.get_id()}")
        print(f"[5] Password hash from DB: {doctor.password[:15]}...")  # Log first 15 chars for security

        # Password verification
        password_valid = check_password_hash(doctor.password, password)
        print(f"[6] Password check result: {'VALID' if password_valid else 'INVALID'}")

        if not password_valid:
            print(f"[ERROR] Password mismatch for doctor: {doctor.get_id()}")
            return jsonify({'error': 'Invalid credentials'}), 401

        # Login user
        login_user(doctor, remember=True, force=True)
        session['_fresh'] = True
        print(f"[7] User logged in successfully - Session started for: {doctor.get_id()}")

        # Prepare response
        response_data = {
            'status': 'success',
            'user_id': doctor.get_id(),
            'role': doctor.role,
            'csrf_token': generate_csrf()
        }
        print("[8] Response data:", response_data)

        response = jsonify(response_data)

        # Set cookies
        response.set_cookie(
            current_app.config['SESSION_COOKIE_NAME'],
            value=doctor.get_id(),
            httponly=True,
            secure=current_app.config['SESSION_COOKIE_SECURE'],
            samesite=current_app.config['SESSION_COOKIE_SAMESITE'],
            max_age=current_app.config['PERMANENT_SESSION_LIFETIME']
        )
        print("[9] Session cookie set via Flask-Login")
        print("[10] Login process completed successfully")
        print("Session contents:", dict(session))

        return response

    except Exception as e:
        print(f"[CRITICAL ERROR] Login failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Успешный выход'})

@auth.route('/check_auth', methods=['GET'])
def check_auth():
    print(f"Session: {session}")  # Для отладки
    return jsonify({
        'is_authenticated': current_user.is_authenticated,
        'user_id': current_user.get_id() if current_user.is_authenticated else None,
        'session_keys': list(session.keys())  # Покажет активные ключи сессии
    })

@auth.route('/session_debug')
def session_debug():
    return jsonify({
        'session_keys': list(session.keys()),
        'user_loaded': current_user.is_authenticated,
        'user_id': current_user.get_id() if current_user.is_authenticated else None
    })

@auth.before_request
def before_request():
    print(f"Current session: {dict(session)}")
    print(f"User loaded: {current_user.is_authenticated}")