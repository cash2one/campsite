from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField, RadioField, ValidationError, TextField, SelectMultipleField
from wtforms.validators import Required, Optional, Email, InputRequired
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import User, Camp_Session

STATES = [('AK','AK'),('AL','AL'),("AR","AR"),("AZ","AZ"),("CA","CA"),("CO","CO"),("CT","CT"),("DC","DC"),("DE","DE"),("FL","FL"),("GA","GA"),("HI","HI"),("IA","IA"),("ID","ID"), ("IL","IL"),("IN","IN"),("KS","KS"),("KY","KY"),("LA","LA"),("MA","MA"),("MD","MD"),("ME","ME"),("MH","MH"),("MI","MI"),("MN","MN"),("MO","MO"),("MS","MS"),("MT","MT"),("NC","NC"),("ND","ND"),("NE","NE"),("NH","NH"),("NJ","NJ"),("NM","NM"),("NV","NV"),("NY","NY"), ("OH","OH"),("OK","OK"),("OR","OR"),("PA","PA"),("PR","PR"),("PW","PW"),("RI","RI"),("SC","SC"),("SD","SD"),("TN","TN"),("TX","TX"),("UT","UT"),("VA","VA"),("VI","VI"),("VT","VT"),("WA","WA"),("WI","WI"),("WV","WV"),("WY","WY")]

GRADES = [(str(i), str(i)) for i in xrange(1,12)]
TSIZES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
ALLERGIES = [('None', 'None'), ('Food', 'Food'), ('Medicine', 'Medicine'), ('Enviornment', 'Enviornment'), ('Insect Bites', 'Insect Bites'), ('Other', 'Other')]
YESNO = [(1, 'Yes'),(0, 'No')]
FDATE = '%m/%d/%Y'

class UpdateParentProfileForm(FlaskForm):
    g1fn = StringField('Guardian 1: First Name', validators=[Required()])
    g1ln = StringField('Guradian 1: Last Name', validators=[Required()])
    g1street = StringField('Guradian 1: Street', validators=[Required()])
    g1city = StringField('Guardian 1: City', validators=[Required()])
    g1state = SelectField('State', choices = STATES, validators=[Required()])
    g1zipcode = StringField('Guardian 1: Zipcode', validators=[Required()])
    g1country = StringField('Guardian 1: Country', default='USA', validators=[Required()])
    g1phone = StringField('Guardian 1: Phone', validators=[Required()])
    g2fn = StringField('Guardian 2: First Name' , validators=[Optional()])
    g2ln = StringField('Guradian 2: Last Name', validators=[Optional()])
    g2street = StringField('Guardian 2: Street', validators=[Optional()])
    g2city = StringField('Guardian 2: City', validators=[Optional()])
    g2state = SelectField('Guardian 2: State', choices = STATES, validators=[Optional()])
    g2zipcode = StringField('Guardian 2: Zipcode', validators=[Optional()])
    g2country = StringField('Guardian 2: Country', default='USA', validators=[Optional()])
    g2phone = StringField('Guardian 2: Phone', validators=[Optional()])
    g2email = StringField('Guardian 2: Email', validators=[Optional()])
    submit = SubmitField('Create/Update Parent Profile')


class CamperRegistrationForm(FlaskForm):
    session = SelectField('Camp Session', choices=Camp_Session.active_sessions(), validators=[Required()])
    gradeinfall = SelectField('Grade in Fall', choices=GRADES, validators=[Required()])
    previouscamper = RadioField('Previous Camper', choices=YESNO, coerce=int, validators=[Optional()])
    tshirtsize = SelectField('T-Shirt Size', choices=TSIZES, validators=[Required()])
    cabinpalname = StringField('Cabin Pal Name', validators=[Optional()])
    emgname = StringField('Emergency Contact Name', validators=[Required()])
    emgrelation = StringField('Relation', validators=[Required()])
    emgphone = StringField('Phone', validators=[Required()])
    emgemail = StringField('Email', validators=[Required(), Email()])
    acceptterms = BooleanField('Accept Terms', validators=[Required()])
    ppsreleaseagreement = BooleanField('Accept Pack Paddle Agreement', validators=[Required()])
    submit = SubmitField('Submit Application')

class MedicationForm(FlaskForm):
    presc = RadioField('Prescription Medication?', choices=YESNO, validators=[Required()])
    name = StringField('Medication Name', validators=[Required()])
    reason = StringField('Reason for taking it', validators=[Required()])
    dosage = StringField('Dosage (include mg)', validators=[Required()])
    schedule = TextField('When is it to be given', validators=[Required()])
    admin = StringField('How is it given (oral, inhaled, nasal, etc...)', validators=[Required()])
    other = TextField('Anything else we should know regarding the medication?', validators=[Optional()])
    submit = SubmitField('Add Medication')

class MedicalForm(FlaskForm):
    allergies = SelectMultipleField('Allergies', choices=ALLERGIES, validators=[InputRequired()])
    dtap = DateField('Diptheria, tetanus, pertussis: DTaP or TDaP', format=FDATE, validators=[InputRequired()])
    mump = DateField('Mump, measels, rubella (MMR)', format=FDATE, validators=[InputRequired()])
    polio = DateField('Polio (IPV)', format=FDATE, validators=[InputRequired()])
    ckpox = DateField('Varicella (chickenpox)', format=FDATE, validators=[InputRequired()])
    meningitis = DateField('Meningococcal meningitis', format=FDATE ,validators=[InputRequired()])
    hib = DateField('Haemophilus influenza B (HIB)', format=FDATE, validators=[InputRequired()])
    pcv = DateField('Pneumococcal (PCV)', format=FDATE, validators=[InputRequired()])
    tb = DateField('Tubercolosis test (TB) (PPD)', format=FDATE, validators=[InputRequired()])
    tbtest = RadioField('Result', coerce=int, choices=[(0, 'neg'),(1, 'positive')], validators=[InputRequired()])
    hosp = RadioField('Ever been hospitalized?', coerce=int, choices=YESNO, validators=[InputRequired()])
    surg = RadioField('Ever had surgery?', coerce=int, choices=YESNO, validators=[InputRequired()])
    chro = RadioField('Have a recurrent/chronic illness?', coerce=int, choices=YESNO, validators=[InputRequired()])
    bedw = RadioField('Had a history of bedwetting?', coerce=int, choices=YESNO, validators=[InputRequired()])
    recinj = RadioField('Had a recent injury?', coerce=int, choices=YESNO, validators=[InputRequired()])
    asth = RadioField('Had asthma/ wheezing/ shortness of bread, Inputrequired an inhaler?', coerce=int, choices=YESNO, validators=[InputRequired()])
    diab = RadioField('Have diabetes?', coerce=int, choices=YESNO, validators=[InputRequired()])
    envallg = RadioField('Had seasonal/ enviornmental allergies?', coerce=int, choices=YESNO, validators=[InputRequired()])
    seiz = RadioField('Had a seizure?', coerce=int, choices=YESNO, validators=[InputRequired()])
    dizz = RadioField('Had fainting or dizziness?', coerce=int, choices=YESNO, validators=[InputRequired()])
    chestpain = RadioField('Passed out/ had chest pain with exercise?', coerce=int, choices=YESNO, validators=[InputRequired()])
    add = RadioField('Ever been treated for attention deficit disorder (ADD)?', coerce=int, choices=YESNO, validators=[InputRequired()])
    emodisorder = RadioField('Ever been treated for emotional and/or behavioral disorder or eating disorder?', coerce=int, choices=YESNO, validators=[InputRequired()])
    seenprof = RadioField('Over the past 12 months, seen a professional for any of the above?', coerce=int, choices=YESNO, validators=[InputRequired()])
    other = RadioField('Had any other issues you would like us to know?', coerce=int, choices=YESNO, validators=[InputRequired()])
    explain = TextField('Please explain "yes" answers:', validators=[Optional()])
    swim = RadioField('Allowed to swim', coerce=int, choices=YESNO, validators=[InputRequired()])
    restrictions = TextField('He/ She may participate in all camp activities, with the following restrictions (which parents will be responsible for discussign with camp staff/ counselor upon arrival to camp, to assure tehse restrictions are able to be met', validators=[Optional()])
    insu = RadioField('This camper is covered by family medical/hospital insurance', coerce=int, choices=YESNO, validators=[InputRequired()])
    insucomp = StringField('Insurance Company')
    insupoli = StringField('Policy Number')
    insusubs = StringField('Subscriber')
    insuphone = StringField('Insurance Company Phone Number')
    sign = BooleanField('Check to Sign', validators=[Required()])
    parent = StringField('Parent who filled this form', validators=[Required()])
    submit = SubmitField('Submit Medical Form')


class UpdateCamperProfileForm(FlaskForm):
    fn = StringField('First Name', validators=[Required()])
    ln = StringField('Last Name', validators=[Required()])
    dob = DateField('Date of Birth', format=FDATE, validators=[Required()])
    gender = RadioField('Gender', choices=[('M', 'Male'),('F', 'Female')], validators=[Required()])
    street = StringField('Street', validators=[Required()])
    state = SelectField('State', choices = STATES, validators=[Required()])
    country = StringField('Country', default = "USA", validators=[Required()])
    zipcode = StringField('Zipcode', validators=[Required()])
    campercell = StringField('Camper Cell', validators=[Optional()])
    camperemail = StringField('Camper Email', validators=[Optional(),Email()])
    submit = SubmitField('Add/Update Camper')