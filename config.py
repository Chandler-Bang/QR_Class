import os
import sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess what'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
'mysql+pymysql://root:chinaren110@localhost:3306/QRclass'


config = {
    'production': Config
}
