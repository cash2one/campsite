from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
# from ..email import send_email
from .forms import LoginForm, CreateAccountForm
    # ChangePasswordForm,\
    # PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    errors = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Logging In: {0}'.format(form.email.data))
            # Change this to users logged in screen
            return redirect(url_for('dashboard'))
        else:
            errors = [form.email.errors, form.password.errors]
    return render_template('auth/login.html', form=form, errors=errors)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return render_template('home.html')


@auth.route('/register', methods=['GET','POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        # send_email(user.email. .... etc)
        flash('Account Created for {0}'.format(form.email.data))
        return redirect(url_for('auth.login'))
    return render_template('auth/create_account.html', form=form)



