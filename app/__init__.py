# Import flask and template operators
from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)

from app import controller, models

