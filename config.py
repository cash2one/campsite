DEBUG = True

# Set app directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
# Production DB
# SQLALCHEMY_DATABASE_URI = 'mysql://hhscusername:freepassword@hhscdb.ci7xsupmx76b.us-east-1.rds.amazonaws.com/hhscdb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

# print __file__

THREADS_PER_PAGE = 2

# Protection against Cross-site Request Forgery (CSRF)
WTF_CSRF_ENABLED = True

# CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"