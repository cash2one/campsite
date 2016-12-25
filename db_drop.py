#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
# from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path
db.session.remove()
db.session.close()
db.session.drop_all()