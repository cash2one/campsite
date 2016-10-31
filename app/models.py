from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import request, url_for


class Camp_Session(db.Model):
    __tablename__ = 'camp_session'
    id = db.Column(db.Integer, primary_key = True)
    session = db.Column(db.Integer)
    year = db.Column(db.String(4))
    camper_registrations = db.relationship('Camper_Registration', backref='camp_session',lazy='dynamic')
    counselor_registrations = db.relationship('Counselor_Registration', backref='camp_session', lazy='dynamic')

    def __repr__(self):
        return '<{0} Session {1}>'.format(self.year, self.session)

class Camper(db.Model):
    __tablename__ = 'camper'
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    birthdate = db.Column(db.Date, index = True)
    camp_session_id = db.Column(db.Integer, db.ForeignKey('camp_session.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))

    def __repr__(self):
        return '<Camper {0} {1}>'.format(self.firstname, self.lastname)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    parents_id = db.Column(db.Integer, db.ForeignKey('parents.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Parents(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key = True)
    fatherfn = db.Column(db.String(64), index = True)
    fatherln = db.Column(db.String(64), index = True)
    motherfn = db.Column(db.String(64), index = True)
    motherln = db.Column(db.String(64), index = True)
    street = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    zipcode = db.Column(db.String(200))
    country = db.Column(db.String(200))
    altstreet = db.Column(db.String(200))
    email = db.Column(db.String, unique = True)
    campers = db.relationship('Camper', backref='parents', lazy='dynamic')

    def __repr__(self):
        return '<Parent {0} {1}>'.format(self.firstname, self.lastname)


class Camper_Registration(db.Model):
    __tablename__ = 'camper_registration'
    id = db.Column(db.Integer, primary_key = True)
    camper_id = db.Column(db.Integer, db.ForeignKey('camper.id'))
    camp_session_id = db.Column(db.Integer, db.ForeignKey('camp_session.id'))
    medical_form_id = db.Column(db.Integer, db.ForeignKey('medical_form.id'))
    submission_timestamp = db.Column(db.DateTime)
    payment_received = db.Column(db.DateTime)
    registration_complete = db.Column(db.Boolean)
    accepted = db.Column(db.Boolean)

    def __repr__(self):
        return '<Registration record {0}>'.format(self.camper_id)

class Medical_Form(db.Model):
    __tablename__ = 'medical_form'
    id = db.Column(db.Integer, primary_key = True)
    vaccine = db.Column(db.String(500))

class Counselor_Registration(db.Model):
    __tablename__ = 'counselor_registration'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.DateTime)
    camp_session_id = db.Column(db.Integer, db.ForeignKey('camp_session.id'))