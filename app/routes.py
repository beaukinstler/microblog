from flask import render_template_string, render_template, request, flash, redirect, after_this_request
from flask import current_app, url_for, send_from_directory
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
import random, string, json
from flask import make_response, session as login_session
from app.youtube import getmp3
import pdb
import os

MP3DIR = app.config['MP3DIR']


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
        link = request.form['link']
        result = getmp3(link)
        if result['error'] != '':
            flash(result['error'])
            return redirect(url_for('mp3maker'))
        flash('You converted "{}" into "{}_{}.mp3"'.format(
                result['video_title'], result['video_id'], result['video_title']))
        return redirect(url_for('download', vid_id=result['video_id']))

    else:
        state = get_state_token()
        login_session['state'] = state

        # # remove any old files if not set to keep files
        if not app.config['KEEPMP3S']:
            uploads = os.path.join(current_app.root_path, MP3DIR)
            files_arr = os.listdir("./app/" + MP3DIR)
            for file in files_arr:
                filename = uploads + "/" + file
                try:

                    print("Purging {}".format(filename))
                    os.remove(filename)
                except Exception as e:
                    print(e)

        return render_template('getmp3.html', title='Mp3 maker', STATE=state )


@app.route('/mp3s/<path:vid_id>', methods=['GET', 'POST'])
def download(vid_id):
    files_arr = os.listdir("./app/" + MP3DIR)
    for file in files_arr:
        if vid_id in file:
            filename = str(file)
            break
        else:
            flash('Could not file video with ID "{}"'.format(vid_id))
            return redirect(url_for('mp3maker'))

    uploads = os.path.join(current_app.root_path, MP3DIR)
    print("DEBUG: Files uploads is - {} and filename is - {}".format(uploads, filename))
    return send_from_directory(uploads, filename, as_attachment=True)

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