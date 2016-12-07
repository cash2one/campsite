from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField, RadioField, ValidationError, TextField, SelectMultipleField
from wtforms.validators import Required, Optional, Email
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import User, Camp_Session

STATES = [('AK','AK'),('AL','AL'),("AR","AR"),("AZ","AZ"),("CA","CA"),("CO","CO"),("CT","CT"),("DC","DC"),("DE","DE"),("FL","FL"),("GA","GA"),("HI","HI"),("IA","IA"),("ID","ID"), ("IL","IL"),("IN","IN"),("KS","KS"),("KY","KY"),("LA","LA"),("MA","MA"),("MD","MD"),("ME","ME"),("MH","MH"),("MI","MI"),("MN","MN"),("MO","MO"),("MS","MS"),("MT","MT"),("NC","NC"),("ND","ND"),("NE","NE"),("NH","NH"),("NJ","NJ"),("NM","NM"),("NV","NV"),("NY","NY"), ("OH","OH"),("OK","OK"),("OR","OR"),("PA","PA"),("PR","PR"),("PW","PW"),("RI","RI"),("SC","SC"),("SD","SD"),("TN","TN"),("TX","TX"),("UT","UT"),("VA","VA"),("VI","VI"),("VT","VT"),("WA","WA"),("WI","WI"),("WV","WV"),("WY","WY")]

GRADES = [(str(i), str(i)) for i in xrange(1,12)]
TSIZES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
ALLERGIES = [('0', 'None'), ('1', 'Food'), ('2', 'Medicine'), ('3', 'Enviornment'), ('4', 'Insect Bites'), ('5', 'Other')]
YESNO = [(True, 'Yes'),(False, 'No')]

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
    previouscamper = RadioField('Previous Camper', choices=[('Yes','Yes'), ('No','No')], validators=[Optional()])
    tshirtsize = SelectField('T-Shirt Size', choices=TSIZES, validators=[Required()])
    cabinpalname = StringField('Cabin Pal Name', validators=[Optional()])
    emgname = StringField('emgname', validators=[Required()])
    emgrelation = StringField('emgrelation', validators=[Required()])
    emgphone = StringField('emgphone', validators=[Required()])
    emgemail = StringField('emgemail', validators=[Required(), Email()])
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
    allergies = SelectMultipleField('Allergies', choices=ALLERGIES, validators=[Required()])
    dtap = DateField('Diptheria, tetanus, pertussis: DTaP or TDaP', validators=[Required()])
    mump = DateField('Mump, measels, rubella (MMR)', validators=[Required()])
    polio = DateField('Polio (IPV)', validators=[Required()])
    ckpox = DateField('Varicella (chickenpox)', validators=[Required()])
    meningitis = DateField('Meningococcal meningitis', validators=[Required()])
    hib = DateField('Haemophilus influenza B (HIB)', validators=[Required()])
    pcv = DateField('Pneumococcal (PCV)', validators=[Required()])
    tb = DateField('Tubercolosis test (TB) (PPD)', validators=[Required()])
    tbtest = RadioField('Result', choices=[(False, 'neg'),(True, 'positive')])
    hosp = BooleanField('Ever been hospitalized?', validators=[Required()])
    surg = BooleanField('Ever had surgery?', validators=[Required()])
    chro = BooleanField('Have a recurrent/chronic illness?', validators=[Required()])
    bedw = BooleanField('Had a history of bedwetting?', validators=[Required()])
    recinj = BooleanField('Had a recent injury?', validators=[Required()])
    asth = BooleanField('Had asthma/ wheezing/ shortness of bread, required an inhaler?', validators=[Required()])
    diab = BooleanField('Have diabetes?', validators=[Required()])
    envallg = BooleanField('Had seasonal/ enviornmental allergies?', validators=[Required()])
    seiz = BooleanField('Had a seizure?', validators=[Required()])
    dizz = BooleanField('Had fainting or dizziness?', validators=[Required()])
    chestpain = BooleanField('Passed out/ had chest pain with exercise?', validators=[Required()])
    add = BooleanField('Ever been treated for attention deficit disorder (ADD)?', validators=[Required()])
    emodisorder = BooleanField('Ever been treated for emotional and/or behavioral disorder or eating disorder?', validators=[Required()])
    seenprof = BooleanField('Over the past 12 months, seen a professional for any of the above?', validators=[Required()])
    other = BooleanField('Had any other issues you would like us to know?', validators=[Required()])
    explain = TextField('Please explain "yes" answers:)', validators=[Optional()])
    swim = RadioField('Allowed to swim', choices=YESNO, validators=[Required()])
    restrictions = TextField('He/ She may participate in all camp activities, with the following restrictions (which parents will be responsible for discussign with camp staff/ counselor upon arrival to camp, to assure tehse restrictions are able to be met', validators=[Optional()])
    insu = RadioField('This camper is covered by family medical/hospital insurance', choices=YESNO)
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
    dob = DateField('Date of Birth', validators=[Required()])
    gender = RadioField(choices=[('M', 'Male'),('F', 'Female')], validators=[Required()])
    street = StringField('Street', validators=[Required()])
    state = SelectField('State', choices = STATES, validators=[Required()])
    country = StringField('Country', default = "USA", validators=[Required()])
    zipcode = StringField('Zipcode', validators=[Required()])
    campercell = StringField('Camper Cell', validators=[Optional()])
    camperemail = StringField('Camper Email', validators=[Optional(),Email()])
    submit = SubmitField('Add/Update Camper')