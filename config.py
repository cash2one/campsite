DEBUG = True

# Set app directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# Production DB
# SQLALCHEMY_DATABASE_URI = 'mysql://hhscusername:freepassword@hhscdb.ci7xsupmx76b.us-east-1.rds.amazonaws.com/hhscdb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

# print __file__

THREADS_PER_PAGE = 5

# email server
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 587
MAIL_USERNAME = 'hhsc.register@gmail.com'
MAIL_PASSWORD = 'weeks2+2'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEBUG = True
MAIL_DEFAULT_SENDER = 'hhsc.register@gmail.com'
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = True
MAIL_ASCII_ATTACHMENTS = False
# administrator list
ADMINS = ['ankurtoshniwal4@gmail.com']

# Protection against Cross-site Request Forgery (CSRF)
WTF_CSRF_ENABLED = True

# CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"