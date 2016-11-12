from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField, RadioField, ValidationError
from wtforms.validators import Required, Optional, Email
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import User, Camp_Session

STATES = [('AK','AK'),('AL','AL'),("AR","AR"),("AZ","AZ"),("CA","CA"),("CO","CO"),("CT","CT"),("DC","DC"),("DE","DE"),("FL","FL"),("GA","GA"),("HI","HI"),("IA","IA"),("ID","ID"), ("IL","IL"),("IN","IN"),("KS","KS"),("KY","KY"),("LA","LA"),("MA","MA"),("MD","MD"),("ME","ME"),("MH","MH"),("MI","MI"),("MN","MN"),("MO","MO"),("MS","MS"),("MT","MT"),("NC","NC"),("ND","ND"),("NE","NE"),("NH","NH"),("NJ","NJ"),("NM","NM"),("NV","NV"),("NY","NY"), ("OH","OH"),("OK","OK"),("OR","OR"),("PA","PA"),("PR","PR"),("PW","PW"),("RI","RI"),("SC","SC"),("SD","SD"),("TN","TN"),("TX","TX"),("UT","UT"),("VA","VA"),("VI","VI"),("VT","VT"),("WA","WA"),("WI","WI"),("WV","WV"),("WY","WY")]

GRADES = [(str(i), str(i)) for i in xrange(12)]
TSIZES = [('Small', 'S'), ('Medium', 'M'), ('Large', 'L')]

class UpdateParentProfileForm(FlaskForm):
    g1fn = StringField('Guardian 1: First Name', validators=[Required()])
    g1ln = StringField('Guradian 1: Last Name', validators=[Required()])
    g2fn = StringField('Guardian 2: First Name' , validators=[Optional()])
    g2ln = StringField('Guradian 2: Last Name', validators=[Optional()])
    g1street = StringField('Guradian 1: Street', validators=[Required()])
    g1city = StringField('Guardian 1: City', validators=[Required()])
    g1state = SelectField('State', choices = STATES, validators=[Required()])
    g1zipcode = StringField('Guardian 1: Zipcode', validators=[Required()])
    g1country = StringField('g1country', validators=[Required()])
    g2street = StringField('g1street', validators=[Optional()])
    g2city = StringField('g1city', validators=[Optional()])
    g2state = SelectField('State', choices = STATES, validators=[Optional()])
    g2zipcode = StringField('g1zipcode', validators=[Optional()])
    g2country = StringField('g1country', validators=[Optional()])
    g1phone = StringField('g1phone', validators=[Required()])
    g2phone = StringField('g2phone', validators=[Optional()])
    g1email = StringField('g1email', validators=[Required()])
    g2email = StringField('g2email', validators=[Optional()])
    submit = SubmitField('Create/Update Parent Profile')

def active_sessions():
    return Camp_Session.query.filter_by(year='2016')

class CamperRegistrationForm(FlaskForm):
    session = QuerySelectField('Camp Session', query_factory=active_sessions, validators=[Required()])
    gradeinfall = SelectField('Grade in Fall', choices=GRADES, validators=[Required()])
    previouscamper = RadioField('Previous Camper', choices=[('Yes','Yes'), ('No','No')], validators=[Optional()])
    tshirtsize = SelectField('T-Shirt Size', choices=TSIZES, validators=[Required()])
    cabinpalname = StringField('Cabin Pal Name', validators=[Optional()])
    emgname = StringField('emgname', validators=[Required()])
    emgrelation = StringField('emgrelation', validators=[Required()])
    emgphone = StringField('emgphone', validators=[Required()])
    emgemail = StringField('emgemail', validators=[Required()])
    acceptterms = BooleanField('Accept Terms', validators=[Required()])
    ppsreleaseagreement = BooleanField('Accept Pack Paddle Agreement', validators=[Required()])



class UpdateCamperProfileForm(FlaskForm):
    fn = StringField('First Name', validators=[Required()])
    ln = StringField('Last Name', validators=[Required()])
    dob = DateField('Date of Birth', validators=[Required()])
    gender = RadioField(choices=[('M', 'Male'),('F', 'Female')], validators=[Required()])
    street = StringField('Street', validators=[Required()])
    state = SelectField('State', choices = STATES, validators=[Required()])
    country = StringField('Country', default = "USA", validators=[Required()])
    zipcode = StringField('Zipcode', validators=[Required()])
    campercell = StringField('Camper Cell', validators=[Optional()])
    camperemail = StringField('Camper Email', validators=[Optional(),Email()])
    submit = SubmitField('Add Camper')