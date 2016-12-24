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
admin = Admin(app, name='campsite', template_mode='bootstrap3')
mail = Mail(app)
principals = Principal(app)

from app import controller, models

# pagedown = PageDown(app)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# protect a view with a principal for that need

from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    can_export = True

class CamperRegistrationModelView(ModelView):
    can_export = True
    # edit_template = 'admin/registration_edit.html'
    # list_template = 'admin/registration_list.html'
    inline_models = [models.Medical_Form,]

class MedicalFormModelView(ModelView):
    can_export = True

class CamperModelView(ModelView):
    can_export = True
    column_searchable_list = ('fn', 'ln', 'dob')

class ParentsModelView(ModelView):
    inline_models = (models.Camper,)

admin.add_view(UserModelView(models.User, db.session))
admin.add_view(CamperRegistrationModelView(models.Camper_Registration, db.session))
admin.add_view(ModelView(models.Camp_Session, db.session))
admin.add_view(CamperModelView(models.Camper, db.session))
admin.add_view(ParentsModelView(models.Parents, db.session))
admin.add_view(MedicalFormModelView(models.Medical_Form, db.session))