# Import flask and template operators
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask import Blueprint
# from flask_pagedown import PageDown

# Define the WSGI application object
app = Flask(__name__)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
mail = Mail(app)
# pagedown = PageDown(app)
app.config.from_object('config')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from app import controller, models

