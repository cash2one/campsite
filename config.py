DEBUG = True

# Set app directory
import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Production DBS
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ankur:weeks2+2@hhsc.citqsa4cgxcw.us-east-1.rds.amazonaws.com:3306/website'
# SQLALCHEMY_DATABASE_URI = 'postgres://otxfbmyruvjrqp:be285e1a17020371dc63cfd88debf4a52f46129506422333fa54ce7ce32be994@ec2-54-225-118-55.compute-1.amazonaws.com:5432/d4lolf30b4fm4m'
# SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

# print __file__

THREADS_PER_PAGE = 5

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'hhsc.register@gmail.com'
MAIL_PASSWORD = 'July&2sessions'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = False
MAIL_ASCII_ATTACHMENTS = False
# administrator list
ADMINS = ['ankurtoshniwal4@gmail.com']
APPLICATION_ROOT = "omhhsc.org"

# Protection against Cross-site Request Forgery (CSRF)
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_SECRET_KEY = "145qqkjelrkn2345h9HNSEMqffhsw5y5"

CSRF_SESSION_KEY = "BASDboasdfkjewrBASD"

SECRET_KEY = "ASDFLKERJAaskdjfewoir5"