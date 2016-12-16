from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import request, url_for
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy.orm import relationship, backref

allergies = [(1,'No Allergies'), (2, 'Food'), (3, 'Medicine'),(4,'Enviornment'),(5,'Insect Bites'),(6,'Other')]

class Camp_Session(db.Model):
    __tablename__ = 'camp_session'
    id = db.Column(db.Integer, primary_key = True)
    session = db.Column(db.Integer)
    year = db.Column(db.String(4))
    camper_registrations = db.relationship('Camper_Registration', backref='camp_session',lazy='dynamic')
    counselor_registrations = db.relationship('Counselor_Registration', backref='camp_session', lazy='dynamic')

    @classmethod
    def active_sessions(self):
        current_year = str(datetime.now().year)
        sessions = Camp_Session.query.filter_by(year=current_year).all()
        if sessions != None:
            sessions = [(str(s.id), "Session {0} {1}".format(str(s.session), s.year)) for s in sessions]
        print sessions
        return sessions

    @classmethod
    def registration_active(self):
        current_year = str(datetime.now().year)
        sessions = Camp_Session.query.filter_by(year=current_year).first()
        if sessions is None:
            return False
        else:
            return True

    def __repr__(self):
        return '<{0} Session {1}>'.format(self.year, self.session)

class Camper(db.Model):
    __tablename__ = 'camper'
    id = db.Column(db.Integer, primary_key = True)
    fn = db.Column(db.String(64), index=True)
    ln = db.Column(db.String(64), index=True)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(5))
    street = db.Column(db.String(200))
    state = db.Column(db.String(2))
    country = db.Column(db.String(64))
    zipcode = db.Column(db.String(8))
    campercell = db.Column(db.String(64))
    camperemail = db.Column(db.String(64))
    parents_id = db.Column(db.Integer, db.ForeignKey('parents.id'))

    regs = db.relationship('Camper_Registration', backref='camper', lazy='dynamic')

    def find_active_registration(self):
        current_year = str(datetime.now().year)
        regs = Camper_Registration.query.filter_by(camper_id=self.id).join(Camp_Session, Camper_Registration.camp_session_id==Camp_Session.id).filter_by(year=current_year).first()
        return regs

    @property
    def age(self):
        return ((datetime.now().date() - self.dob).days) / 365
    

    def __repr__(self):
        return '<Camper {0} {1}>'.format(self.fn, self.ln)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    parents = db.relationship('Parents', backref='user', uselist=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id).first()
    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': self.id})

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('confirm') != self.id:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True

    # def generate_reset_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.id})
'''
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True
'''
    # def generate_email_change_token(self, new_email, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'change_email': self.id, 'new_email': new_email})

    # def change_email(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return False
    #     if data.get('change_email') != self.id:
    #         return False
    #     new_email = data.get('new_email')
    #     if new_email is None:
    #         return False
    #     if self.query.filter_by(email=new_email).first() is not None:
    #         return False
    #     self.email = new_email
    #     self.avatar_hash = hashlib.md5(
    #         self.email.encode('utf-8')).hexdigest()
    #     db.session.add(self)
    #     return True

    # def can(self, permissions):
    #     return self.role is not None and \
    #         (self.role.permissions & permissions) == permissions

    # def is_administrator(self):
    #     return self.can(Permission.ADMINISTER)

    # def generate_auth_token(self, expiration):
    # s = Serializer(current_app.config['SECRET_KEY'],
    #                expires_in=expiration)
    # return s.dumps({'id': self.id}).decode('ascii')

class Parents(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True)
    g1fn = db.Column(db.String(64), index = True)
    g1ln = db.Column(db.String(64), index = True)
    g2fn = db.Column(db.String(64), index = True)
    g2ln = db.Column(db.String(64), index = True)
    g1street = db.Column(db.String(64))
    g1city = db.Column(db.String(64))
    g1state = db.Column(db.String(64))
    g1zipcode = db.Column(db.String(64))
    g1country = db.Column(db.String(64))
    g2street = db.Column(db.String(64))
    g2city = db.Column(db.String(64))
    g2state = db.Column(db.String(64))
    g2zipcode = db.Column(db.String(64))
    g2country = db.Column(db.String(64))
    g1phone = db.Column(db.String(64))
    g2phone = db.Column(db.String(64))
    g2email = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    campers = db.relationship('Camper', backref='parents', lazy='dynamic')

    def __repr__(self):
        return '<Parents {0}>'.format(self.g1ln)


class Camper_Registration(db.Model):
    __tablename__ = 'camper_registration'
    id = db.Column(db.Integer, primary_key = True)
    submission_timestamp = db.Column(db.TIMESTAMP)
    payment_received = db.Column(db.TIMESTAMP)
    registration_complete = db.Column(db.Boolean)
    accepted = db.Column(db.Boolean)
    camper_id = db.Column(db.Integer, db.ForeignKey('camper.id'))
    camp_session_id = db.Column(db.Integer, db.ForeignKey('camp_session.id'))
    gradeinfall = db.Column(db.String(2))
    prevcamper = db.Column(db.Boolean)
    cabin_pal_name = db.Column(db.String(64))
    shirtsize = db.Column(db.String(4))
    emgname = db.Column(db.String(255))
    emgrelation = db.Column(db.String(64))
    emgemail = db.Column(db.String(64))
    emgphone = db.Column(db.String(32))
    accept = db.Column(db.Integer)
    ppsrelease = db.Column(db.Boolean)

    med_form = db.relationship('Medical_Form', backref=backref("camper_registration", uselist=False))

    def __repr__(self):
        camper = Camper.query.get(self.camper_id)
        return '<Registration for {0} - id:{1}>'.format(camper.fn, self.id)

    def get_session(self):
        session = Camp_Session.query.get(self.camp_session_id)
        return "Session {0}".format(session.session)

    @property
    def sub_time(self):
        return self.submission_timestamp.strftime("%I:%M:%S%p %m/%d/%y")

class Medical_Form(db.Model):

    __tablename__ = 'medical_form'
    id = db.Column(db.Integer, primary_key = True)
    allergies = db.Column(db.String(1024))
    dtap = db.Column(db.Date)
    mump = db.Column(db.Date)
    polio = db.Column(db.Date)
    ckpox = db.Column(db.Date)
    meningitis = db.Column(db.Date)
    hib = db.Column(db.Date)
    pcv = db.Column(db.Date)
    tb = db.Column(db.Date)
    tbtest =db.Column(db.Boolean)
    hosp = db.Column(db.Boolean)
    surg = db.Column(db.Boolean)
    chro = db.Column(db.Boolean)
    bedw = db.Column(db.Boolean)
    recinj = db.Column(db.Boolean)
    asth = db.Column(db.Boolean)
    envallg = db.Column(db.Boolean)
    diab = db.Column(db.Boolean)
    seiz = db.Column(db.Boolean)
    dizz = db.Column(db.Boolean)
    chestpain = db.Column(db.Boolean)
    add = db.Column(db.Boolean)
    emodisorder = db.Column(db.Boolean)
    seenprof = db.Column(db.Boolean)
    other = db.Column(db.Boolean)
    explain = db.Column(db.String(1024))
    swim = db.Column(db.Boolean)
    restrictions = db.Column(db.String(1024))
    insu = db.Column(db.Boolean)
    insucomp = db.Column(db.String(128))
    insupoli = db.Column(db.String(128))
    insusubs = db.Column(db.String(128))
    insuphon = db.Column(db.String(128))
    sign = db.Column(db.Boolean)
    parent = db.Column(db.String(128))
    submission_timestamp = db.Column(db.TIMESTAMP)
    camper_registration_id = db.Column(db.Integer, db.ForeignKey('camper_registration.id'))

    prescriptions = db.relationship('Medication', backref='medications', lazy='dynamic')

    def __repr__(self):
        return '<Medical Form {0}>'.format(self.id)

    @property
    def sub_time(self):
        return self.submission_timestamp.strftime("%I:%M:%S%p %m/%d/%y")

class Medication(db.Model):

    __tablename__ = 'medication'
    id = db.Column(db.Integer, primary_key = True)
    medical_id = db.Column(db.Integer, db.ForeignKey('medical_form.id'))
    name = db.Column(db.String(512))
    reason = db.Column(db.String(2000))
    dosage = db.Column(db.String(128))
    schedule = db.Column(db.String(512))
    admin = db.Column(db.String(512))
    other = db.Column(db.String(512))

    def __repr__(self):
        return '<Medication {0}'.format(self.id)


class Counselor_Registration(db.Model):
    __tablename__ = 'counselor_registration'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.DateTime)
    camp_session_id = db.Column(db.Integer, db.ForeignKey('camp_session.id'))