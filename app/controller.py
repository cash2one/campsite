from flask import render_template
from app import app

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_pages/not_found.html'), 404

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html') 
