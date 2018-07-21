from flask import render_template_string, render_template, request, flash, redirect
from app import app
from app.forms import LoginForm

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

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested from {}, and remember_me  = {}".format(
                form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
