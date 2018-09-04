from flask import render_template_string, render_template, request, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
import random, string, json
from flask import make_response, session as login_session
from app.youtube import getmp3
import pdb



@app.route('/')
@app.route('/index')
@login_required
def index():
    """ 
    Test data for initial testing phase
    """
    # user = {'username': 'Beau'}
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
    return render_template('index.html',title='Home',posts=posts)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Umm, that's not correct")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/getmp3',methods=['GET', 'POST'])
@login_required
def mp3maker():
    """
    Purpose:    A page to post a link, and call YoutubeDL to convert 
                a video into an mp3.
    """
    
    if request.method == 'POST':
        getmp3()
        return redirect(url_for('mp3maker'))  # TODO: this should really go to a page to download the file, or I should find a way to just download the file
        
    else:
        state = get_state_token()
        login_session['state'] = state
        return render_template('getmp3.html', title='Mp3 maker', STATE=state )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))




"""
Helper functions:
"""
def get_state_token():
    """
    Create a random string for use with state tokens for CRSF protection
    """
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    return token

def bad_state(request_token, session_token):
    """
    Purpose: Check if the request has the proper state token

    Returns: A response object.  If the state is valid, the response
             is returned with 'None' as the value.
    """
    if request.form['state'] != login_session['state']:
            response = make_response(json.dumps('Invalid state parameter.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'

    else:
        response = None

    return response