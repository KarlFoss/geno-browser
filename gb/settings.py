from datetime import timedelta

DEBUG = True
SECRET_KEY = 'temporary_secret_key' # make sure to change this
JWT_AUTH_URL_RULE = '/api/auth'
JWT_EXPIRATION_DELTA = timedelta(hours=24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///gb.db'