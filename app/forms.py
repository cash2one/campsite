from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class CreateAccountForm(Form):
    g1fn = StringField('g1fn', validators=[DataRequired()])
    g1ln = StringField('g1ln', validators=[DataRequired()])
    g2fn = StringField('g2fn')
    g2ln = StringField('g2ln')
    g1street = StringField('g1street', validators=[DataRequired()])
    g1city = StringField('g1city', validators=[DataRequired()])
    g1state = StringField('g1state', validators=[DataRequired()])
    g1zipcode = StringField('g1zipcode', validators=[DataRequired()])
    g1country = StringField('g1country', validators=[DataRequired()])
    g2street = StringField('g1street')
    g2city = StringField('g1city')
    g2state = StringField('g1state')
    g2zipcode = StringField('g1zipcode')
    g2country = StringField('g1country')
    g1phone = StringField('g1phone', validators=[DataRequired()])
    g2phone = StringField('g2phone')
    g1email = StringField('g1email', validators=[DataRequired()])
    g2email = StringField('g2email')

class ParentProfileForm(Form):
    g1email = StringField('g1email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class CamperRegistrationForm(Form):
    session
    gradeinfall
    previouscamper
    tshirtsize
    cabinpalname notreq
    emgname = StringField('emgname', validators=[DataRequired()])
    emgrelation = StringField('emgrelation', validators=[DataRequired()])
    emgphone = StringField('emgphone', validators=[DataRequired()])
    emgemail = StringField('emgemail', validators=[DataRequired()])
    phyname
    phyphone
    phyaddress
    acceptterms = BooleanField
    ppsreleaseagreement = BooleanField

class AddCamper(Form):
    lastname
    firstname
    dob
    gender
    street
    state
    country
    zipcode
    campercell = optional
    cameremail = optional