# Import flask and template operators
from flask import Flask
from flask_bootstrap import Bootstrap

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
Bootstrap(app)

from app import controller

# Configurations
app.config.from_object('config')

