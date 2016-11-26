from flask import render_template, flash, redirect, url_for
from app import app
from .forms import UpdateParentProfileForm, UpdateCamperProfileForm, CamperRegistrationForm, MedicalForm
from flask_login import login_required, current_user
from .models import *
from datetime import datetime

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/not_found.html'), 404

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

@app.route('/update_parent_profile/<int:parents_id>', methods=['GET', 'POST'])
@login_required
def edit_parent_profile(parents_id):
    form = UpdateParentProfileForm()
    parents = Parents.query.get(parents_id)
    form.g1fn.default = parents.g1fn
    form.g1ln.default = parents.g1ln
    form.g2fn.default = parents.g2fn
    form.g2ln.default = parents.g2ln
    form.g1street.default = parents.g1street
    form.g1city.default = parents.g1city
    form.g1state.default = parents.g1state
    form.g1zipcode.default = parents.g1zipcode
    form.g1country.default = parents.g1country
    form.g2street.default = parents.g2street
    form.g2city.default = parents.g2city
    form.g2state.default = parents.g2state
    form.g2zipcode.default = parents.g2zipcode
    form.g2country.default = parents.g2country
    form.g1phone.default = parents.g1phone
    form.g2phone.default = parents.g2phone
    form.g2email.default = parents.g2email
    if form.validate_on_submit():
        

    current_user.id

@app.route('/parent_profile', methods=['GET', 'POST'])
@login_required
def update_parent_profile():
    form = UpdateParentProfileForm()
    if form.validate_on_submit():
        parents = Parents(
            g1fn = form.g1fn.data,
            g1ln = form.g1ln.data,
            g2fn = form.g2fn.data,
            g2ln = form.g2ln.data,
            g1street = form.g1street.data,
            g1city = form.g1city.data,
            g1state = form.g1state.data,
            g1zipcode = form.g1zipcode.data,
            g1country = form.g1country.data,
            g2street = form.g2street.data,
            g2city = form.g2city.data,
            g2state = form.g2state.data,
            g2zipcode = form.g2zipcode.data,
            g2country = form.g2country.data,
            g1phone = form.g1phone.data,
            g2phone = form.g2phone.data,
            g2email = form.g2email.data,
            user_id = current_user.id
            )
        db.session.add(parents)
        db.session.commit()
        flash('Parent Profile Created')
        return redirect(url_for('dashboard'))
    return render_template('parent_profile.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    parents = Parents.query.filter_by(user_id=current_user.id).first()
    if parents is None:
        return redirect(url_for('update_parent_profile'))
    campers = Camper.query.filter_by(parents_id=current_user.parents.id).all()
    regs = {c:c.find_active_registration() for c in campers}
    sess = {}
    for c in campers:
        if regs[c] == "None":
            sess[c] = "None"
        else:
            sess[c] = Camp_Session.query.get(regs[c].camp_session_id)

    return render_template('dashboard.html', campers=campers, regs=regs, sess=sess)

@app.route('/camper_profile', methods=['GET','POST'])
@login_required
def add_camper():
    form = UpdateCamperProfileForm()
    errors = None
    if form.validate_on_submit():
        camper = Camper(
            fn = form.fn.data,
            ln = form.ln.data,
            dob = form.dob.data,
            gender = form.gender.data,
            street = form.street.data,
            state = form.state.data,
            country = form.country.data,
            zipcode = form.zipcode.data,
            campercell = form.campercell.data,
            camperemail = form.camperemail.data,
            parents_id = current_user.parents.id
            )
        db.session.add(camper)
        db.session.commit()
        flash("Camper {0} added".format(form.fn.data))
        return redirect(url_for('dashboard'))
    return render_template('camper_profile.html', form=form, errors=errors)

@app.route('/register_camper/<int:camper_id>', methods=['GET','POST'])
@login_required
def register_camper(camper_id):
    form = CamperRegistrationForm()
    errors = None
    if form.validate_on_submit():
        camper_registration = Camper_Registration(
            submission_timestamp = datetime.now(),
            camper_id = camper_id,
            camp_session_id = form.session.data,
            gradeinfall = form.gradeinfall.data,
            prevcamper = form.previouscamper.data,
            cabin_pal_name = form.cabinpalname.data,
            shirtsize = form.tshirtsize.data,
            emgname = form.emgname.data,
            emgrelation = form.emgname.data,
            emgemail = form.emgemail.data,
            accept = form.acceptterms.data,
            ppsrelease = form.ppsreleaseagreement.data
            )
        db.session.add(camper_registration)
        db.session.commit()
        flash('Camper Registered')
        return redirect(url_for('dashboard'))
    camper = Camper.query.filter_by(id=camper_id).first()
    return render_template('register_camper.html', form=form, errors=errors, camper=camper)

@app.route('/medical_form/<int:camper_id>', methods=['GET', 'POST'])
@login_required
def medical_form(camper_id):
    form = MedicalForm()
    flash("Reached Medical Form")
    return redirect(url_for('dashboard'))