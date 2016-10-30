from app import db


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