from flask import render_template_string, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Beau'}
    return render_template('index.html',user=user,title='Home')