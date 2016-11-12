from flask import render_template, flash, redirect, url_for
from app import app
from .forms import UpdateParentProfileForm, UpdateCamperProfileForm, CamperRegistrationForm
from flask_login import login_required, current_user
from .models import *

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/not_found.html'), 404

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

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
            g1email = form.g1email.data,
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
    return render_template('dashboard.html', campers=campers)

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
        camper_registration = 1
        flash('Camper Registered')
        return redirect(url_for('dashboard'))
    camper = Camper.query.filter_by(id=camper_id).first()
    return render_template('register_camper.html', form=form, errors=errors, camper=camper)

@app.route('/medical_form/<int:camper_id>', methods=['GET', 'POST'])
@login_required
def medical_form(camper_id):
    flash("Reached Medical Form")
    return redirect(url_for('dashboard'))