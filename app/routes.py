from flask import render_template_string, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Beau'}
    posts = [
        {
            'author': {'username':'Beau'},
            'body':"Beautiful day in Brooklyn, NY"
        },
        {
            'author': {'username':'Uaeb'},
            'body': 'It\'s a real treat'
        }
    ]
    return render_template('index.html',user=user,title='Home',posts=posts)