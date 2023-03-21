import os
from decouple import config
from datetime import timedelta




BASE_DIR = os.path.dirname(os.path.realpath(__file__))

uri = config('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

class Config():
    SECRET_KEY= config('SECRET_KEY','secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes = 30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevConfig:
    DEBUG = config('DEBUG',True, cast = bool)
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'db.sqlite3')



class TestConfig(Config):
    pass
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)
    SQLALCHEMY_DATABASE_URI = uri
    

config_dict = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}