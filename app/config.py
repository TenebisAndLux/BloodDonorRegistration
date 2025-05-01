import os


class Config(object):
    HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    USER = os.environ.get('POSTGRES_USER', 'postgres')
    PASSWD = os.environ.get('POSTGRES_PASSWORD', 'ZeRg1011')
    DB_NAME = os.environ.get('POSTGRES_DB', 'DonorMirror')
    PORT = os.environ.get('POSTGRES_PORT', '5432')

    SECRET_KEY = 'asdhauidkcjoiqdwadsdg43'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWD}@{HOST}:{PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
