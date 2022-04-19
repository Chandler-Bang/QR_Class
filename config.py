import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess what'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'mysql+pymysql://root:chinaren@localhost:3306/QRclass'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
