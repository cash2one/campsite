from flask import render_template, flash, redirect, url_for
from app import app, mail
from .forms import UpdateParentProfileForm, UpdateCamperProfileForm, CamperRegistrationForm, MedicalForm, MedicationForm
from flask_login import login_required, current_user
from .models import *
from datetime import datetime, timedelta
from emails import send_email
from ._helpers import flash_errors, to_bool
from flask import Response
from flask_principal import Principal, Permission, RoleNeed
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers, expose
from flask_admin import Admin
from flask.ext import admin
from werkzeug.wrappers import BaseRequest
from werkzeug.exceptions import HTTPException, NotFound, Unauthorized

admin_permission = Permission(RoleNeed('admin'))
siteroot = 'omhhsc.org'

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/medicalassistant')
def medicalassistant():
    return render_template('medicalassistant.html')

@app.route('/boardoftrustees')
def boardoftrustees():
    return render_template('boardoftrustees.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/assistantmanager')
def assistantmanager():
    return render_template('assistantmanager.html')

@app.route('/campinformation')
def information():

    # Compute values for dashboard
    sess1 = Camp_Session.query.filter_by(year=str(datetime.today().year), session=1).first()
    sess2 = Camp_Session.query.filter_by(year=str(datetime.today().year), session=2).first()

    # Build table for session 1
    if sess1 is None:
        regs1male = 0
        regs1female = 0
    else:
        regs1male = sess1.camper_registrations.filter_by(accepted=1).join(Camper, Camper_Registration.camper_id==Camper.id).filter_by(gender='Male').count()
        regs1female = sess1.camper_registrations.filter_by(accepted=1).join(Camper, Camper_Registration.camper_id==Camper.id).filter_by(gender='Female').count()

    # Build table for session 2
    if sess2 is None:
        regs2male = 0
        regs2female = 0
    else:
        regs2male = sess2.camper_registrations.filter_by(accepted=1).join(Camper, Camper_Registration.camper_id==Camper.id).filter_by(gender='Male').count()
        regs2female = sess2.camper_registrations.filter_by(accepted=1).join(Camper, Camper_Registration.camper_id==Camper.id).filter_by(gender='Female').count()
        
    return render_template('information.html',  regs2female=regs2female, regs2male=regs2male, regs1male=regs1male, regs1female=regs1female, sess1=sess1, sess2=sess2)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/directors')
def directors():
    return render_template('directors.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/fees')
def fees():
    return render_template('fees.html')

@app.route('/facilities')
def facilities():
    return render_template('facilities.html')

@app.route('/kys')
def kys():
    return render_template('kys.html')

@app.route('/counselor')
def counselor():
    return render_template('counselor.html')

@app.route('/update_parent_profile/<int:parents_id>', methods=['GET', 'POST'])
@login_required
def edit_parent_profile(parents_id):
    parents = Parents.query.get(parents_id)

    # Check authorization
    if current_user.parents != parents:
        raise Unauthorized()

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
    flash_errors(form)
    return render_template('parent_profile.html', form=form, edit='True', parents_id=parents.id)

@app.route('/add_parent_profile', methods=['GET', 'POST'])
@login_required
def create_parent_profile():
    parents = Parents.query.filter_by(user_id=current_user.id).first()

    # Do not allow user to add additional parent profiles, only edit current
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
        send_email("Account Created!", recipients=[current_user.email], html_body="<p> Dear {0} {1}, <br> <br> Thank you for creating an HHSC Camper Registration Account. <br> <br>Please note that for the Registration Process to be complete, we must receive the <i> registration form</i>, the <i>medical form</i>, and the <i>full <a href='{2}'>camp fees</a></i>. After the Registration Process is complete, we will inform you of whether your camper has secured a spot in the selected session or is waitlisted.  <br> <br>Thank you, <br>HHSC Administration <p>".format(current_user.parents.g1fn, current_user.parents.g1ln, siteroot + url_for('fees')))
        flash('Parent Profile Created')
        return redirect(url_for('dashboard'))
    return render_template('parent_profile.html', form=form, edit='False')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    parents = Parents.query.filter_by(user_id=current_user.id).first()

    # Force user to create parent profile before proceeding to dashboard
    if parents is None:
        return redirect(url_for('create_parent_profile'))

    # Query database for all dashboard content
    campers = Camper.query.filter_by(parents_id=current_user.parents.id).all()
    regs = {c:c.find_active_registration() for c in campers}
    med = {}
    sess = {}
    pay = {}
    for c in campers:
        if regs[c] is None:
            med[c] = None
            sess[c] = 'None'
            pay[c] = 'None'
        else:
            sess[c] = regs[c].get_session()
            med[c] = Medical_Form.query.filter_by(camper_registration_id=regs[c].id).first()
            if regs[c].payment_received is None:
                pay_received = 'Not Received'
            else:
                pay_received = str(regs[c].payment_received)
            if regs[c].payment_status is None:
                pay_status = ''
            else:
                pay_status = str(regs[c].payment_status)

            pay[c] = [pay_received, '$' + str(regs[c].payment_amount), pay_status]
        # print str(regs[c].payment_received)

    return render_template('dashboard.html', campers=campers, regs=regs, sess=sess, med=med, pay=pay)

@app.route('/edit_camper_profile/<int:camper_id>', methods=['GET','POST'])
@login_required
def edit_camper(camper_id):
    camper = Camper.query.get(camper_id)
    # Check authorization
    if current_user.parents.campers.filter_by(id=camper_id).first() is None:
        raise Unauthorized()

    form = UpdateCamperProfileForm(obj=camper)
    errors = None
    if form.validate_on_submit():
        camper.fn = form.fn.data
        camper.ln = form.ln.data
        camper.dob = form.dob.data
        camper.gender = form.gender.data
        camper.street = form.street.data
        camper.city = form.city.data
        camper.state = form.state.data
        camper.country = form.country.data
        camper.zipcode = form.zipcode.data
        camper.campercell = form.campercell.data
        camper.camperemail = form.camperemail.data
        db.session.commit()
        flash('Camper Profile Updated')
        return redirect(url_for('dashboard'))
    return render_template('camper_profile.html', form=form, errors=errors, edit='True', camper_id=camper.id)

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
            city = form.city.data,
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
    return render_template('camper_profile.html', form=form, errors=errors, edit='False')

@app.route('/register_camper/<int:camper_id>', methods=['GET','POST'])
@login_required
def register_camper(camper_id):
    # Check authorization
    if current_user.parents.campers.filter_by(id=camper_id).first() is None:
        raise Unauthorized()

    reg = Camper.query.get(camper_id).find_active_registration()
    # Do not allow user to add additional registrations if they've already registered
    if reg is not None:
        return redirect(url_for('edit_registration', reg_id=reg.id))

    if not Camp_Session.registration_active():
        flash('No active sessions. Please wait till the New Year to Register')
        return redirect(url_for('dashboard'))

    form = CamperRegistrationForm()
    camper = Camper.query.filter_by(id=camper_id).first()
    errors = None
    if form.validate_on_submit():
        camper_registration = Camper_Registration(
            submission_timestamp = datetime.now(),
            camper_id = camper_id,
            camp_session_id = form.session.data,
            gradeinfall = form.gradeinfall.data,
            prevcamper = to_bool(form.previouscamper.data),
            cabin_pal_name = form.cabinpalname.data,
            shirtsize = form.tshirtsize.data,
            emgname = form.emgname.data,
            emgrelation = form.emgrelation.data,
            emgemail = form.emgemail.data,
            emgphone = form.emgphone.data,
            travel = form.travel.data,
            accept = form.acceptterms.data,
            payment_amount = 0
            )
        session = Camp_Session.query.get(camper_registration.camp_session_id)
        send_email("HHSC Registration {0} {1} - {2}".format(camper.fn, camper.ln, session.formatdate), recipients=[current_user.email, 'hhsc.register@gmail.com'], html_body="<p> Dear {0} {1}, <br> <br> Thank you for registering <b>{2} {3} to HHSC {6}</b>. Please note that to complete the registration process, you must submit the following by <b>{4}</b> or forfeit your child's position in the Queue: <br> <br> 1.  Medical Form (must be filled out online by parent) <br>2.  Full <a href='{5}'>Camp Fees</a> (Check) <br> <br> The Full Registration Fee is to be sent by First Class mail to <br> <br> <center> Hema Bhaskaran <br>HHSC Treasurer <br>8 Tenbury Way  <br>Fairport, NY 14450 </center><br><br><em> Note: HHSC can only accept 57 boys and 57 girls for each session. After the Registration Process is complete, we will inform you of whether your camper has secured a spot in the above selected session or is waitlisted. </em> <br> <br> <b> Important Travel Information </b> <br>If your child is traveling by flight, bus or train and needs transportation between the airport/bus/train terminal and the camp grounds then please be sure to fill out the <a href='https://goo.gl/forms/WTcyOzk3wSnz90hX2'>HHSC Travel Form</a> with their travel information by no later than June 1. <em> Note: There are pick up and drop off <a href='{5}'>transportation fees</a>. Please include the travel fees along with your camper fees or send a check as soon as your travel plans have been made.  </em> <br> <br>Thank you, <br>HHSC Administration <p>".format(current_user.parents.g1fn, current_user.parents.g1ln, camper.fn, camper.ln, (datetime.today() + timedelta(days=14)).strftime('%B %d, %Y'), siteroot + url_for('fees'), session.formatdate))

        db.session.add(camper_registration)
        db.session.commit()
        flash('Camper Registered')
        return redirect(url_for('dashboard'))
    print to_bool(form.previouscamper.data)
    flash_errors(form)
    return render_template('register_camper.html', edit='False', form=form, errors=errors, camper=camper)

@app.route('/edit_camper_registration/<int:reg_id>', methods=['GET','POST'])
@login_required
def edit_registration(reg_id):
    # Check authorization
    if current_user.parents.campers.join(Camper_Registration, Camper.id ==Camper_Registration.camper_id).filter_by(id=reg_id).first() is None:
        raise Unauthorized()

    reg = Camper_Registration.query.get(reg_id)
    form = CamperRegistrationForm(obj=reg)
    errors = None
    print type(to_bool(form.previouscamper.data))
    if form.validate_on_submit():
        reg.camp_session_id = form.session.data
        reg.gradeinfall = form.gradeinfall.data
        reg.prevcamper = to_bool(form.previouscamper.data)
        reg.cabin_pal_name = form.cabinpalname.data
        reg.shirtsize = form.tshirtsize.data
        reg.emgname = form.emgname.data
        reg.emgrelation = form.emgrelation.data
        reg.emgemail = form.emgemail.data
        reg.emgphone = form.emgphone.data
        reg.accept = form.acceptterms.data
        reg.travel = form.travel.data
        db.session.commit()
        flash('Camper Registeration Updated')
        return redirect(url_for('dashboard'))
    flash_errors(form)
    camper = Camper.query.get(reg.camper_id)
    return render_template('register_camper.html', form=form, edit='True', errors=errors, camper=camper, reg_id=reg.id)

@app.route('/edit_medical_form/<int:med_id>', methods=['GET','POST'])
@login_required
def edit_medical_form(med_id):
    mf = Medical_Form.query.get(med_id)

    # Check authorization
    if mf.camper_registration.camper.parents.user != current_user:
        raise Unauthorized()

    form = MedicalForm(obj=mf)
    if form.validate_on_submit():
        mf.allergies = str(form.allergies.data)
        mf.dtap = form.dtap.data
        mf.mump = form.mump.data
        mf.polio = form.polio.data
        mf.ckpox = form.ckpox.data
        mf.meningitis = form.meningitis.data
        mf.hib = form.hib.data
        mf.pcv = form.pcv.data
        mf.tb = form.tb.data
        mf.tbtest = to_bool(form.tbtest.data)
        mf.hosp = to_bool(form.hosp.data)
        mf.surg = to_bool(form.surg.data)
        mf.chro = to_bool(form.chro.data)
        mf.bedw = to_bool(form.bedw.data)
        mf.recinj = to_bool(form.recinj.data)
        mf.asth = to_bool(form.asth.data)
        mf.envallg = to_bool(form.envallg.data)
        mf.diab = to_bool(form.diab.data)
        mf.seiz = to_bool(form.seiz.data)
        mf.dizz = to_bool(form.dizz.data)
        mf.chestpain = to_bool(form.chestpain.data)
        mf.add = to_bool(form.add.data)
        mf.emodisorder = to_bool(form.emodisorder.data)
        mf.seenprof = to_bool(form.seenprof.data)
        mf.other = to_bool(form.other.data)
        mf.explain = form.explain.data
        mf.swim = to_bool(form.swim.data)
        mf.restrictions = form.restrictions.data
        mf.insu = to_bool(form.insu.data)
        mf.insucomp = form.insucomp.data
        mf.insupoli = form.insupoli.data
        mf.insusubs = form.insusubs.data
        mf.insuphon = form.insuphone.data
        mf.sign = form.sign.data
        mf.parentrelation = form.parentrelation.data
        mf.presmeds = to_bool(form.presmeds.data)
        mf.pmed1name = form.pmed1name.data
        mf.pmed1reason = form.pmed1reason.data
        mf.pmed1dosage = form.pmed1dosage.data
        mf.pmed1time = form.pmed1time.data
        mf.pmed1admin = form.pmed1admin.data
        mf.pmed2name = form.pmed2name.data
        mf.pmed2reason = form.pmed2reason.data
        mf.pmed2dosage = form.pmed2dosage.data
        mf.pmed2time = form.pmed2time.data
        mf.pmed2admin = form.pmed2admin.data
        mf.pmed3name = form.pmed3name.data
        mf.pmed3reason = form.pmed3reason.data
        mf.pmed3dosage = form.pmed3dosage.data
        mf.pmed3time = form.pmed3time.data
        mf.pmed3admin = form.pmed3admin.data
        mf.pmed4name = form.pmed4name.data
        mf.pmed4reason = form.pmed4reason.data
        mf.pmed4dosage = form.pmed4dosage.data
        mf.pmed4time = form.pmed4time.data
        mf.pmed4admin = form.pmed4admin.data
        mf.nonpresmeds = to_bool(form.nonpresmeds.data)
        mf.npmed1name = form.npmed1name.data
        mf.npmed1reason = form.npmed1reason.data
        mf.npmed1dosage = form.npmed1dosage.data
        mf.npmed1time = form.npmed1time.data
        mf.npmed1admin = form.npmed1admin.data
        mf.npmed2name = form.npmed2name.data
        mf.npmed2reason = form.npmed2reason.data
        mf.npmed2dosage = form.npmed2dosage.data
        mf.npmed2time = form.npmed2time.data
        mf.npmed2admin = form.npmed2admin.data
        mf.npmed3name = form.npmed3name.data
        mf.npmed3reason = form.npmed3reason.data
        mf.npmed3dosage = form.npmed3dosage.data
        mf.npmed3time = form.npmed3time.data
        mf.npmed3admin = form.npmed3admin.data
        mf.npmed4name = form.npmed4name.data
        mf.npmed4reason = form.npmed4reason.data
        mf.npmed4dosage = form.npmed4dosage.data
        mf.npmed4time = form.npmed4time.data
        mf.npmed4admin = form.npmed4admin.data
        db.session.commit()
        flash('Medical Form Updated')
        return redirect(url_for('dashboard'))
    print "Invalid Submission"
    flash_errors(form)
    camper = Camper.query.get(mf.camper_registration.camper_id)
    return render_template('medical_form.html', mform=form, camper=camper, edit='True', med_id=med_id)

@app.route('/medical_form/<int:camper_id>', methods=['GET', 'POST'])
@login_required
def medical_form(camper_id):

    # Check authorization
    camper = Camper.query.get(camper_id)
    if camper.parents.user != current_user:
        raise Unauthorized()

    reg = camper.find_active_registration()
    if reg is None:
        flash('Register Camper before filling out Medical Form')
        return redirect(url_for('register_camper', camper_id=camper_id))

    med = Medical_Form.query.filter_by(camper_registration_id=reg.id).first()
    if med is not None:
        return redirect(url_for('edit_medical_form', med_id=med.id))

    mform = MedicalForm()
    if mform.submit.data and mform.validate_on_submit():
        med_form = Medical_Form(
            allergies = str(mform.allergies.data),
            allexplain = mform.allexplain.data,
            dtap = mform.dtap.data,
            mump = mform.mump.data,
            polio = mform.polio.data,
            ckpox = mform.ckpox.data,
            hadckpox = mform.hadckpox.data,
            meningitis = mform.meningitis.data,
            hib = mform.hib.data,
            pcv = mform.pcv.data,
            tb = mform.tb.data,
            tbtest = to_bool(mform.tbtest.data),
            hosp = to_bool(mform.hosp.data),
            surg = to_bool(mform.surg.data),
            chro = to_bool(mform.chro.data),
            bedw = to_bool(mform.bedw.data),
            recinj = to_bool(mform.recinj.data),
            asth = to_bool(mform.asth.data),
            envallg = to_bool(mform.envallg.data),
            diab = to_bool(mform.diab.data),
            seiz = to_bool(mform.seiz.data),
            dizz = to_bool(mform.dizz.data),
            chestpain = to_bool(mform.chestpain.data),
            add = to_bool(mform.add.data),
            emodisorder = to_bool(mform.emodisorder.data),
            seenprof = to_bool(mform.seenprof.data),
            other = to_bool(mform.other.data),
            explain = mform.explain.data,
            genexplain = mform.genexplain.data,
            swim = to_bool(mform.swim.data),
            restrictions = mform.restrictions.data,
            insu = to_bool(mform.insu.data),
            insucomp = mform.insucomp.data,
            insupoli = mform.insupoli.data,
            insusubs = mform.insusubs.data,
            insuphon = mform.insuphone.data,
            sign = mform.sign.data,
            datesigned = mform.dateofsign.data,
            parentrelation = mform.parentrelation.data,
            presmeds = to_bool(mform.presmeds.data),
            pmed1name = mform.pmed1name.data,
            pmed1reason = mform.pmed1reason.data,
            pmed1dosage = mform.pmed1dosage.data,
            pmed1time = mform.pmed1time.data,
            pmed1admin = mform.pmed1admin.data,
            pmed2name = mform.pmed2name.data,
            pmed2reason = mform.pmed2reason.data,
            pmed2dosage = mform.pmed2dosage.data,
            pmed2time = mform.pmed2time.data,
            pmed2admin = mform.pmed2admin.data,
            pmed3name = mform.pmed3name.data,
            pmed3reason = mform.pmed3reason.data,
            pmed3dosage = mform.pmed3dosage.data,
            pmed3time = mform.pmed3time.data,
            pmed3admin = mform.pmed3admin.data,
            pmed4name = mform.pmed4name.data,
            pmed4reason = mform.pmed4reason.data,
            pmed4dosage = mform.pmed4dosage.data,
            pmed4time = mform.pmed4time.data,
            pmed4admin = mform.pmed4admin.data,
            nonpresmeds = to_bool(mform.nonpresmeds.data),
            npmed1name = mform.npmed1name.data,
            npmed1reason = mform.npmed1reason.data,
            npmed1dosage = mform.npmed1dosage.data,
            npmed1time = mform.npmed1time.data,
            npmed1admin = mform.npmed1admin.data,
            npmed2name = mform.npmed2name.data,
            npmed2reason = mform.npmed2reason.data,
            npmed2dosage = mform.npmed2dosage.data,
            npmed2time = mform.npmed2time.data,
            npmed2admin = mform.npmed2admin.data,
            npmed3name = mform.npmed3name.data,
            npmed3reason = mform.npmed3reason.data,
            npmed3dosage = mform.npmed3dosage.data,
            npmed3time = mform.npmed3time.data,
            npmed3admin = mform.npmed3admin.data,
            npmed4name = mform.npmed4name.data,
            npmed4reason = mform.npmed4reason.data,
            npmed4dosage = mform.npmed4dosage.data,
            npmed4time = mform.npmed4time.data,
            npmed4admin = mform.npmed4admin.data,
            submission_timestamp = datetime.now(),
            camper_registration_id = reg.id
        )
        camper = Camper.query.get(camper_id)
        session = Camp_Session.query.get(reg.camp_session_id)
        email_body = "<p> Dear {0} {1}, <br> <br>We have received the online medical form for <b>{2} {3} to HHSC {4}</b>. <br> <br> Please note that for the Registration Process to be complete, we must receive the <i> registration form</i>, the <i>medical form</i>, and the <i>full <a href='{5}'>camp fees</a></i>. After the Registration Process is complete, we will inform you of whether your camper has secured a spot in the selected session or is waitlisted.  <br> <br><b> Important Travel Information </b> <br>If your child is traveling by flight, bus or train and needs transportation between the airport/bus/train terminal and the camp grounds then please be sure to fill out the <a href='https://goo.gl/forms/WTcyOzk3wSnz90hX2'>HHSC Travel Form</a> with their travel information by no later than June 1. <em> Note: There are pick up and drop off <a href='{5}'>transportation fees</a>. Please include the travel fees along with your camper fees or send a check as soon as your travel plans have been made.  </em> <br> <br> Thank you, <br> HHSC Administration <p>".format(current_user.parents.g1fn, current_user.parents.g1ln, camper.fn, camper.ln, session.formatdate, siteroot + url_for('fees'))
        send_email("HHSC Medical Form {0} {1} - {2}".format(camper.fn, camper.ln, session.formatdate), recipients=[current_user.email, 'hhsc.register@gmail.com'], html_body=email_body)
        db.session.add(med_form)
        db.session.commit()
        flash("Medical Form Submitted")
        return redirect(url_for('dashboard'))
    flash_errors(mform)
    return render_template('medical_form.html', mform=mform, camper=camper, edit='False')

"""
Admin page contents
"""

# class MyAdminIndexView(admin.AdminIndexView):

#     @expose('/')
#     def index(self):
#         if not current_user.is_authenticated() or current_user.email != 'hhsc.register@gmail.com':
#             return redirect(url_for('auth.login'))
#         return super(MyAdminIndexView, self).index()

class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.email == 'hhsc.register@gmail.com'

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class UserModelView(MyModelView):
    can_export = True
    column_list = ['parents.g1ln', 'parents.g1fn','email', 'password_hash']
    column_searchable_list = ['email']
    column_labels = dict(user_parents_g1ln='Last Name')
    page_size = 50

class CamperRegistrationModelView(MyModelView):
    can_export = True
    edit_template = 'admin/registration_edit.html'
    # list_template = 'admin/registration_list.html'
    # Calculate age of camper at camp
    column_searchable_list = ['camper.fn', 'camper.ln', 'camper.parents.user.email']
    column_list = ["submission_timestamp", 'camper.fn', 'camper.ln', 'camper.dob', 'camper.gender', 'camp_session.formatdate', 'camper.parents.user.email', 'payment_received', 'payment_amount', 'payment_status', 'accepted', 'gradeinfall', 'prevcamper', 'cabin_pal_name', 'shirtsize', 'emgname', 'emgrelation', 'emgemail', 'emgphone', 'travel', 'accept']
    column_labels = dict(payment_email='Send Payment Email?')
    page_size = 50

    def after_model_change(self, form, model, is_created):
        parents = model.camper.parents
        if model.accepted == 1:
            send_email('HHSC Registration Accepted: {0} {1} - {2}'.format(model.camper.fn, model.camper.ln, model.camp_session.formatdate), recipients=['hhsc.register@gmail.com', parents.user.email], html_body="<p> Dear {0} {1}, <br> <br>{2} {3} has been <b>accepted</b> to HHSC <b>{4}</b>.<br><br><b> Important Travel Information </b> <br>If your child is traveling by flight, bus or train and needs transportation between the airport/bus/train terminal and the camp grounds then please be sure to fill out the <a href='https://goo.gl/forms/WTcyOzk3wSnz90hX2'>HHSC Travel Form</a> with their travel information by no later than June 1. <em> Note: There are pick up and drop off <a href='{5}'>transportation fees</a>. Please include the travel fees along with your camper fees or send a check as soon as your travel plans have been made.  </em> <br><br> <b> Important Camp Information</b> <br>Please visit the <a href='{6}'>Camp Website</a> to view a list of what to pack for your child. <br><a href='https://drive.google.com/open?id=0Bx2Zk7UlXDv4LV9FSVVZdjQzdXM'>Click here</a> to view detailed information for enrolled campers <br> <br> Thank you, <br> HHSC Administration <p>".format(parents.g1fn, parents.g1ln, model.camper.fn, model.camper.ln, model.camp_session.formatdate, siteroot + url_for('fees'), siteroot + url_for('information')), attach=url_for('static', filename='pdf/ImportantInformationforEnrolledCampers.pdf'))
        elif model.accepted == -1:
            send_email('HHSC Registration Waitlisted: {0} {1} - {2}'.format(model.camper.fn, model.camper.ln, model.camp_session.formatdate), recipients=['hhsc.register@gmail.com', parents.user.email], html_body="<p> Dear {0} {1}, <br> <br> {2} {3} has been <b>waitlisted</b> for HHSC <b>{4}</b>.<br><br> We have reached our maximum capacity for enrollment at this time. However, we have added your child's name to the waitlist and will hold your check until and if a space becomes available. If a space does not become available, we will void your check. <br> <br> If you would like to withdraw your child from the waitlist, Please inform us by email and we will cancel out the check and shred it. <em> <br> <br> We will let you know if there is a status change. </em> <br> <br> Thank you, <br> HHSC Administration <p>".format(parents.g1fn, parents.g1ln, model.camper.fn, model.camper.ln, model.camp_session.formatdate))
        if model.payment_email:
            send_email('HHSC Payment Received: {0} {1} - {2}'.format(model.camper.fn, model.camper.ln, model.camp_session.formatdate), recipients=['hhsc.register@gmail.com', parents.user.email], html_body="<p> Dear {0} {1}, <br> <br>We have received a total payment of ${2} for <b>{3} {4} to HHSC {5}</b>. <br> <br>Please note that for the Registration Process to be complete, we must receive the <i> registration form</i>, the <i>medical form</i>, and the <i>full <a href='{5}'>camp fees</a></i>. After the Registration Process is complete, we will inform you of whether your camper has secured a spot in the selected session or is waitlisted.  <br> <br><b> Important Travel Information </b> <br>If your child is traveling by flight, bus or train and needs transportation between the airport/bus/train terminal and the camp grounds then please be sure to fill out the <a href='https://goo.gl/forms/WTcyOzk3wSnz90hX2'>HHSC Travel Form</a> with their travel information by no later than June 1. <em> Note: There are pick up and drop off <a href='{6}'>transportation fees</a>. Please include the travel fees along with your camper fees or send a check as soon as your travel plans have been made.  </em> <br> <br> Thank you, <br> HHSC Administration <p>".format(parents.g1fn, parents.g1ln, str(model.payment_amount), model.camper.fn, model.camper.ln, model.camp_session.formatdate, siteroot + url_for('fees')))
            model.payment_email = True
            db.session.commit()
    # @expose('/')
    # def index(self):
    #     print 'HELLOOO'
    #     return self.render('admin/registration_list.html')

class MedicalFormModelView(MyModelView):
    can_export = True
    column_searchable_list = ['camper_registration.camper.fn', 'camper_registration.camper.ln', 'camper_registration.camp_session.session']
    column_list = ['submission_timestamp', 'camper_registration.camper.fn', 'camper_registration.camper.ln', 'camper_registration.camper.dob', 'camper_registration.camper.gender', 'camper_registration.camp_session.formatdate', 'allergies','allexplain','dtap','mump','polio','ckpox','hadckpox','meningitis','hib','pcv','tb','tbtest','hosp','surg','chro','bedw','recinj','asth','envallg','diab','seiz','dizz','chestpain','add','genexplain','emodisorder','seenprof','other','explain','swim','restrictions','presmeds','pmed1name','pmed1reason','pmed1dosage','pmed1time','pmed1admin','pmed2name','pmed2reason','pmed2dosage','pmed2time','pmed2admin','pmed3name','pmed3reason','pmed3dosage','pmed3time','pmed3admin','pmed4name','pmed4reason','pmed4dosage','pmed4time','pmed4admin','nonpresmeds','npmed1name','npmed1reason','npmed1dosage','npmed1time','npmed1admin','npmed2name','npmed2reason','npmed2dosage','npmed2time','npmed2admin','npmed3name','npmed3reason','npmed3dosage','npmed3time','npmed3admin','npmed4name','npmed4reason','npmed4dosage','npmed4time','npmed4admin','insu','insucomp','insupoli','insusubs','insuphon','sign','parentrelation','datesigned']
    page_size = 50

class CamperModelView(MyModelView):
    can_export = True
    column_searchable_list = ['fn', 'ln']
    column_list = ['fn', 'ln', 'dob', 'gender', 'street', 'city', 'state', 'zipcode', 'campercell', 'camperemail', 'parents.g1fn', 'parents.g1ln']
    page_size = 50

class ParentsModelView(MyModelView):
    can_export = True
    column_searchable_list = ['g1fn', 'g1ln', 'user.email']
    column_list = ['g1fn', 'g1ln', 'g1street', 'g1city', 'g1state', 'g1zipcode', 'g1country', 'g1phone', 'user.email', 'g2fn', 'g2ln', 'g2street', 'g2city', 'g2state', 'g2zipcode', 'g2country', 'g2phone', 'g2email', 'user.email']
    page_size = 50

class MessageBoardModelView(MyModelView):
    page_size = 50
    can_export = True

class CampSessionModelView(MyModelView):
    page_size = 50
    can_export = True

admin = Admin(app, 'HHSC Admin', template_mode='bootstrap3')

admin.add_view(UserModelView(User, db.session))
admin.add_view(CamperRegistrationModelView(Camper_Registration, db.session))
admin.add_view(CampSessionModelView(Camp_Session, db.session))
admin.add_view(CamperModelView(Camper, db.session))
admin.add_view(ParentsModelView(Parents, db.session))
admin.add_view(MedicalFormModelView(Medical_Form, db.session))
admin.add_view(MessageBoardModelView(Message_Board, db.session))

"""
Error controller links
"""

@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/not_found.html'), 404

@app.errorhandler(401)
def no_permission(error):
    return render_template('error_pages/unauthorized.html'), 401
