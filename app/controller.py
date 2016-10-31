from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/not_found.html'), 404

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Logging In: {0} with password: {1}'.format(form.username.data, form.password.data))
        # Change this to users logged in screen
        return redirect('/')
    return render_template('login.html', username= "trial", password="secret", form=form)


@app.route('/create_account', methods=['POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = Parent
        flash('Account Created for {0}'.format(form.email.data)
        return redirect('/')
    return render_template('create_account.html', form=form)