import os
from datetime import timedelta


class Config(object):
    HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    USER = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWD = os.environ.get('POSTGRES_PASSWORD', 'ZeRg1011')
    DB_NAME = os.environ.get('POSTGRES_DB', 'DonorMirror')
    PORT = os.environ.get('POSTGRES_PORT', '5432')

    SECRET_KEY = 'Flk5$9qoP7@z#Mn2*Xp8vRt6wYb1cNd3'
    SESSION_COOKIE_NAME = 'doctor_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'Lp4$kQ9!zTm2#vR7@yX5sWu6eD8fGh3j'
    WTF_CSRF_TIME_LIMIT = 3600  # 1 час
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWD}@{HOST}:{PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
