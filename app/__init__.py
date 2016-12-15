# Import flask and template operators
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_admin import Admin
from flask import Blueprint
# from flask_pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

# Define the WSGI application object

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
admin = Admin(app, name='campsite', template_mode='bootstrap3')
mail = Mail(app)

from app import controller, models

# pagedown = PageDown(app)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


# email server


from flask_admin.contrib.sqla import ModelView
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Camper_Registration, db.session))
admin.add_view(ModelView(models.Camp_Session, db.session))
admin.add_view(ModelView(models.Camper, db.session))
admin.add_view(ModelView(models.Parents, db.session))
admin.add_view(ModelView(models.Medical_Form, db.session))