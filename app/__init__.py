# Import flask and template operators
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_admin import Admin
from flask import Blueprint
from flask import Flask, Response
from flask.ext.principal import Principal, Permission, RoleNeed

# from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

# Define the WSGI application object

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
adminFlask = Admin(app, name='campsite', template_mode='bootstrap3')
mail = Mail(app)
principals = Principal(app)

from app import controller, models

# pagedown = PageDown(app)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# protect a view with a principal for that need

