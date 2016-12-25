from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, SelectField, RadioField, ValidationError, TextAreaField, SelectMultipleField
from wtforms.validators import Required, Optional, Email, InputRequired
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import User, Camp_Session
from ._formhelpers import MultiCheckboxField
from datetime import datetime

STATES = [('AK','AK'),('AL','AL'),("AR","AR"),("AZ","AZ"),("CA","CA"),("CO","CO"),("CT","CT"),("DC","DC"),("DE","DE"),("FL","FL"),("GA","GA"),("HI","HI"),("IA","IA"),("ID","ID"), ("IL","IL"),("IN","IN"),("KS","KS"),("KY","KY"),("LA","LA"),("MA","MA"),("MD","MD"),("ME","ME"),("MH","MH"),("MI","MI"),("MN","MN"),("MO","MO"),("MS","MS"),("MT","MT"),("NC","NC"),("ND","ND"),("NE","NE"),("NH","NH"),("NJ","NJ"),("NM","NM"),("NV","NV"),("NY","NY"), ("OH","OH"),("OK","OK"),("OR","OR"),("PA","PA"),("PR","PR"),("PW","PW"),("RI","RI"),("SC","SC"),("SD","SD"),("TN","TN"),("TX","TX"),("UT","UT"),("VA","VA"),("VI","VI"),("VT","VT"),("WA","WA"),("WI","WI"),("WV","WV"),("WY","WY")]

GRADES = [('1st','1st'),('2nd','2nd'),('3rd','3rd'),('4th','4th'),('5th','5th'),('6th','6th'),('7th','7th'),('8th','8th'),('9th','9th'),('10th','10th'),('11th','11th'),('12th','12th')]
TSIZES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X Large')]
ALLERGIES = [('None', 'None'), ('Food', 'Food'), ('Medicine', 'Medicine'), ('Enviornment', 'Enviornment'), ('Insect Bites', 'Insect Bites'), ('Other', 'Other')]
YESNO = [(1, 'Yes'),(0, 'No')]
TRAVEL = [('Flight', 'Flight'), ('Bus', 'Bus'), ('Train', 'Train'), ('Own arrangement', 'Own arrangement')]
DOSAGETIMES = [(' ',' '),('Breakfast','Breakfast'),('Lunch','Lunch'),('Dinner','Dinner'),('Bedtime','Bedtime')]
MEDADMIN = [('Oral', 'Oral'),('Nasal', 'Nasal'),('Inhalation', 'Inhalation'),('Injection', 'Injection'),('Other', 'Other')]
FDATE = '%m/%d/%Y'
DATEPH = 'mm/dd/yyyy'
REASON = 'Reason for taking medication'
DOSAGE = 'Including mg'
TIME = 'When it should be given'

class UpdateParentProfileForm(FlaskForm):
    g1fn = StringField('First Name', validators=[Required()])
    g1ln = StringField('Last Name', validators=[Required()])
    g1street = StringField('Street', validators=[Required()])
    g1city = StringField('City', validators=[Required()])
    g1state = StringField('State', validators=[Required()])
    g1zipcode = StringField('Zipcode', validators=[Required()])
    g1country = StringField('Country', default='USA', validators=[Required()])
    g1phone = StringField('Phone', validators=[Required()])
    g2fn = StringField('First Name' , validators=[Required()])
    g2ln = StringField('Last Name', validators=[Required()])
    g2street = StringField('Street', validators=[Required()])
    g2city = StringField('City', validators=[Required()])
    g2state = StringField('State', validators=[Required()])
    g2zipcode = StringField('Zipcode', validators=[Required()])
    g2country = StringField('Country', default='USA', validators=[Required()])
    g2phone = StringField('Phone', validators=[Required()])
    g2email = StringField('Email', validators=[Required()])
    submit = SubmitField('Create/Update Parent Profile')


class CamperRegistrationForm(FlaskForm):
    session = SelectField('Camp Session', choices=Camp_Session.active_sessions(), validators=[Required()])
    gradeinfall = SelectField('Grade in Fall', choices=GRADES, validators=[Required()])
    previouscamper = RadioField('Previous Camper', choices=YESNO, coerce=int, validators=[InputRequired()])
    tshirtsize = SelectField('Adult T-Shirt Size', choices=TSIZES, validators=[InputRequired()])
    cabinpalname = StringField('Cabin Pal Name', validators=[Optional()], render_kw={"placeholder": "Full Name"})
    emgname = StringField('Name', validators=[Required()])
    emgrelation = StringField('Relation', validators=[Required()])
    emgphone = StringField('Phone', validators=[Required()])
    emgemail = StringField('Email', validators=[Required(), Email()])
    travel = SelectField('Mode of Travel', choices=TRAVEL, validators=[Required()])
    acceptterms = BooleanField('Accept Terms', validators=[Required()])
    submit = SubmitField('Submit Application')

class MedicationForm(FlaskForm):
    presc = RadioField('Prescription Medication?', choices=YESNO, validators=[InputRequired()])
    name = StringField('Medication Name', validators=[Required()])
    reason = StringField('Reason for taking it', validators=[Required()])
    dosage = StringField('Dosage (include mg)', validators=[Required()])
    schedule = TextAreaField('When is it to be given', validators=[Required()])
    admin = StringField('How is it given (oral, inhaled, nasal, etc...)', validators=[Required()])
    other = TextAreaField('Anything else we should know regarding the medication?', validators=[Optional()])
    submit = SubmitField('Add Medication')

class MedicalForm(FlaskForm):
    allergies = MultiCheckboxField('Allergies', choices=ALLERGIES, validators=[InputRequired()])
    allexplain = TextAreaField("Explain reactions to all allergies below:", validators=[Optional()])
    dtap = DateField('Diptheria, tetanus, pertussis: DTaP or TDaP', format=FDATE, validators=[InputRequired()], render_kw={"placeholder": DATEPH})
    mump = DateField('Mump, measels, rubella (MMR)', format=FDATE, validators=[InputRequired()], render_kw={"placeholder": DATEPH} )
    polio = DateField('Polio (IPV)', format=FDATE, validators=[InputRequired()], render_kw={"placeholder": DATEPH})
    ckpox = DateField('Varicella (chickenpox)', format=FDATE, validators=[InputRequired()], render_kw={"placeholder": DATEPH})
    hadckpox = DateField('If your child has had Varicella (chickenpox), please enter the date', render_kw={"placeholder": DATEPH}, validators=[Optional()], format=FDATE)
    meningitis = DateField('Meningococcal meningitis (Ages 11 and up)', format=FDATE ,validators=[Optional()], render_kw={"placeholder": DATEPH})
    hib = DateField('Haemophilus influenza B (HIB)', format=FDATE, validators=[Required()], render_kw={"placeholder": DATEPH})
    pcv = DateField('Pneumococcal (PCV)', format=FDATE, validators=[Required()], render_kw={"placeholder": DATEPH})
    tb = DateField('Tubercolosis test (TB) (PPD)', format=FDATE, validators=[Optional()], render_kw={"placeholder": DATEPH})
    tbtest = RadioField('Result', coerce=int, choices=[(0, 'neg'),(1, 'positive')], validators=[Optional()])
    presmeds = RadioField('Does your child take any Daily Prescription Medications?', choices=YESNO, coerce=int, validators=[InputRequired()])
    pmed1name = StringField('Medicaton Name', validators=[Optional()])
    pmed1reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    pmed1dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    pmed1time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    pmed1admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    pmed2name =StringField('Medicaton Name', validators=[Optional()])
    pmed2reason =StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    pmed2dosage =StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    pmed2time =SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    pmed2admin =RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    pmed3name =StringField('Medicaton Name', validators=[Optional()])
    pmed3reason =StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    pmed3dosage =StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    pmed3time =SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    pmed3admin =RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    pmed4name = StringField('Medicaton Name', validators=[Optional()])
    pmed4reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    pmed4dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    pmed4time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    pmed4admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    nonpresmeds = RadioField('Does your child take any Daily Non-Prescription Medications?', choices=YESNO, coerce=int, validators=[InputRequired()])
    npmed1name = StringField('Medicaton Name', validators=[Optional()])
    npmed1reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    npmed1dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    npmed1time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    npmed1admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    npmed2name = StringField('Medicaton Name', validators=[Optional()])
    npmed2reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    npmed2dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    npmed2time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    npmed2admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    npmed3name = StringField('Medicaton Name', validators=[Optional()])
    npmed3reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    npmed3dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    npmed3time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    npmed3admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
    npmed4name = StringField('Medicaton Name', validators=[Optional()])
    npmed4reason = StringField('Reason', validators=[Optional()], render_kw={"placeholder": REASON})
    npmed4dosage = StringField('Dosage', validators=[Optional()], render_kw={"placeholder": DOSAGE})
    npmed4time = SelectField('Time to give', choices=DOSAGETIMES, validators=[Optional()], render_kw={"placeholder": TIME})
    npmed4admin = RadioField('Administration', choices=MEDADMIN, validators=[Optional()])
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
    explain = TextAreaField('Please explain "Yes" answers below:', validators=[Optional()])
    genexplain = TextAreaField('Please explain "Yes" answers below:', validators=[Optional()])
    swim = RadioField('Allowed to swim', coerce=int, choices=YESNO, validators=[InputRequired()])
    restrictions = TextAreaField('He/ She may participate in all camp activities, with the following restrictions (which parents will be responsible for discussing with camp staff/ counselor upon arrival to camp, to assure these restrictions are able to be met)', validators=[Optional()])
    insu = RadioField('This camper is covered by family medical/hospital insurance', coerce=int, choices=YESNO, validators=[InputRequired()])
    insucomp = StringField('Insurance Company')
    insupoli = StringField('Policy Number')
    insusubs = StringField('Subscriber')
    insuphone = StringField('Insurance Company Phone Number')
    sign = StringField('Signature', render_kw={"placeholder": "Full Name"}, validators=[Required()])
    dateofsign = DateField('Date', default=datetime.now(), format=FDATE, validators=[Required()])
    parentrelation = StringField('Relation', validators=[Required()])
    submit = SubmitField('Submit Medical Form')

class UpdateCamperProfileForm(FlaskForm):
    fn = StringField('First Name', validators=[Required()])
    ln = StringField('Last Name', validators=[Required()])
    dob = DateField('Date of Birth', format=FDATE, validators=[Required()], render_kw={"placeholder": DATEPH})
    gender = RadioField('Gender', choices=[('Male', 'Male'),('Female', 'Female')], validators=[Required()])
    street = StringField('Street', validators=[Required()])
    city = StringField('City', validators=[Required()])
    state = StringField('State', validators=[Required()])
    country = StringField('Country', default = "USA", validators=[Required()])
    zipcode = StringField('Zipcode', validators=[Required()])
    campercell = StringField('Camper Cell', validators=[Optional()])
    camperemail = StringField('Camper Email', validators=[Optional(),Email()])
    submit = SubmitField('Add/Update Camper')