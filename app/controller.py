from flask import render_template, flash, redirect, url_for
from app import app
from .forms import UpdateParentProfileForm, UpdateCamperProfileForm, CamperRegistrationForm, MedicalForm, MedicationForm
from flask_login import login_required, current_user
from .models import *
from datetime import datetime

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

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
    parents = Parents.query.get(parents_id)
    form = UpdateParentProfileForm(obj=parents)
    if form.validate_on_submit():
        parents.g1fn = form.g1fn.data
        parents.g1ln = form.g1ln.data
        parents.g2fn = form.g2fn.data
        parents.g2ln = form.g2ln.data
        parents.g1street = form.g1street.data
        parents.g1city = form.g1city.data
        parents.g1state = form.g1state.data
        parents.g1zipcode = form.g1zipcode.data
        parents.g1country = form.g1country.data
        parents.g2street = form.g2street.data
        parents.g2city = form.g2city.data
        parents.g2state = form.g2state.data
        parents.g2zipcode = form.g2zipcode.data
        parents.g2country = form.g2country.data
        parents.g1phone = form.g1phone.data
        parents.g2phone = form.g2phone.data
        parents.g2email = form.g2email.data
        db.session.commit()
        flash('Parent Profile Updated')
        return redirect(url_for('dashboard'))
    return render_template('parent_profile.html', form=form)

@app.route('/add_parent_profile', methods=['GET', 'POST'])
@login_required
def create_parent_profile():
    parents = Parents.query.filter_by(user_id=current_user.id).first()
    if parents is not None:
        return redirect(url_for('edit_parent_profile',parents_id=parents.id))

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
        return redirect(url_for('create_parent_profile'))
    campers = Camper.query.filter_by(parents_id=current_user.parents.id).all()
    regs = {c:c.find_active_registration() for c in campers}
    med = {}
    sess = {}
    for c in campers:
        if regs[c] is None:
            med[c] = None
            sess[c] = "None"
        else:
            sess[c] = regs[c].get_session()
            med[c] = Medical_Form.query.filter_by(camper_registration_id=regs[c].id)

    return render_template('dashboard.html', campers=campers, regs=regs, sess=sess, med=med)

@app.route('/edit_camper_profile/<int:camper_id>', methods=['GET','POST'])
@login_required
def edit_camper(camper_id):
    camper = Camper.query.get(camper_id)
    form = UpdateCamperProfileForm(obj=camper)
    errors = None
    if form.validate_on_submit():
        camper.fn = form.fn.data
        camper.ln = form.ln.data
        camper.dob = form.dob.data
        camper.gender = form.gender.data
        camper.street = form.street.data
        camper.state = form.state.data
        camper.country = form.country.data
        camper.zipcode = form.zipcode.data
        camper.campercell = form.campercell.data
        camper.camperemail = form.camperemail.data
        db.session.commit()
        flash('Camper Profile Updated')
        return redirect(url_for('dashboard'))
    return render_template('camper_profile.html', form=form, errors=errors)


@app.route('/add_camper', methods=['GET','POST'])
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
    reg = Camper.query.get(camper_id).find_active_registration()
    if reg is not None:
        return redirect(url_for('edit_registration', reg_id=reg.id))

    if not Camp_Session.registration_active():
        flash('No active sessions. Please wait till the New Year to Register')
        return redirect(url_for('dashboard'))

    form = CamperRegistrationForm()
    errors = None
    print 'reached validation'
    if form.validate_on_submit():
        print 'inside validate'
        camper_registration = Camper_Registration(
            submission_timestamp = datetime.now(),
            camper_id = camper_id,
            camp_session_id = form.session.data,
            gradeinfall = form.gradeinfall.data,
            prevcamper = form.previouscamper.data,
            cabin_pal_name = form.cabinpalname.data,
            shirtsize = form.tshirtsize.data,
            emgname = form.emgname.data,
            emgrelation = form.emgrelation.data,
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

@app.route('/edit_camper_registration/<int:reg_id>', methods=['GET','POST'])
@login_required
def edit_registration(reg_id):
    reg = Camper_Registration.query.get(reg_id)
    form = CamperRegistrationForm(obj=reg)
    errors = None
    print 'HELLOOO'
    if form.validate_on_submit():
        reg.submission_timestamp = datetime.now()
        reg.camp_session_id = form.session.data
        reg.gradeinfall = form.gradeinfall.data
        reg.prevcamper = form.previouscamper.data
        reg.cabin_pal_name = form.cabinpalname.data
        reg.shirtsize = form.tshirtsize.data
        reg.emgname = form.emgname.data
        reg.emgrelation = form.emgrelation.data
        reg.emgemail = form.emgemail.data
        reg.emgphone = form.emgphone.data
        reg.accept = form.acceptterms.data
        reg.ppsrelease = form.ppsreleaseagreement.data
        db.session.commit()
        flash('Camper Registeration Updated')
        print 'HELLOOOO'
        return redirect(url_for('dashboard'))
    print 'Invalid form'
    flash_errors(form)
    camper = Camper.query.get(reg.camper_id)
    return render_template('register_camper.html', form=form, errors=errors, camper=camper)

@app.route('/medical_form/<int:camper_id>', methods=['GET', 'POST'])
@login_required
def medical_form(camper_id):
    reg = Camper.query.get(camper_id).find_active_registration()
    if reg is None:
        flash('Register Camper before filling out Medical Form')
        return redirect(url_for('register_camper', camper_id=camper_id))

    print "about to call MedicationForm"
    mform = MedicalForm()
    pform = MedicationForm()
    if mform.validate_on_submit() and mform.submit:
        med_form = Medical_Form(
            allergies = mform.allergies.data,
            dtap = mform.dtap.data,
            mump = mform.mump.data,
            polio = mform.polio.data,
            ckpox = mform.ckpox.data,
            meningitis = mform.meningitis.data,
            hib = mform.hib.data,
            pcv = mform.pcv.data,
            tb = mform.tb.data,
            tbtest =mform.tbtest.data,
            hosp = mform.hosp.data,
            surg = mform.surg.data,
            chro = mform.chro.data,
            bedw = mform.bedw.data,
            recinj = mform.recinj.data,
            asth = mform.asth.data,
            envallg = mform.envallg.data,
            diab = mform.diab.data,
            seiz = mform.seiz.data,
            dizz = mform.dizz.data,
            chestpain = mform.chestpain.data,
            add = mform.add.data,
            emodisorder = mform.emodisorder.data,
            seenprof = mform.seenprof.data,
            other = mform.other.data,
            explain = mform.explain.data,
            swim = mform.swim.data,
            restrictions = mform.restrictions.data,
            insu = mform.insu.data,
            insucomp = mform.insucomp.data,
            insupoli = mform.insupoli.data,
            insusubs = mform.insusubs.data,
            insuphon = mform.insuphon.data,
            sign = mform.sign.data,
            parent = mform.parent.data,
            submission_timestamp = datetime.now(),
            camper_registration_id = reg.id
        )
        db.session.add(med_form)
        db.session.commit()
        flash("Medical Form Submitted")
        return redirect(url_for('dashboard'))
    flash_errors(mform)
    return render_template('medical_form.html', mform = mform, pform=pform, camper_id=camper_id)