from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm,\
        ResetPasswordRequestForm, ResetPasswordForm, DenialForm,\
        PollingPlaceFinder
from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse
from app.models import User, Post, Denial
from datetime import datetime
from app.email import send_password_reset_email
from flask import g
from flask_babel import get_locale
import app.civic as civic
import os
from flask import session as post_session
from app import utilities as utl

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().\
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    #  Pagination links
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    if form.validate_on_submit():
        post = Post(body=form.post_body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('index'))
    else:
        return render_template('index.html', title='Home',
                               form=form, posts=posts.items,
                               next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You're now one of us...")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/user')
@app.route('/user/')
@login_required
def user_redirect():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    else:
        flash("Please log in")
        return redirect(url_for('login'))


@app.route('/users')
@app.route('/users/')
@login_required
def users():
    if current_user.is_authenticated:
        users = db.session.query(User).filter(
                User.username != current_user.username).limit(50)
        return render_template('users.html', users=users)
    else:
        flash("Please log in")
        return redirect(url_for('login'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('basic_form.html', title=form.title, form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).\
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    #  Pagination links
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/denied', methods=['GET', 'POST'])
def denied():
    """
    Gather and show data for denied logs
    """
    elections = civic.get_election_names()
    elections.reverse()
    form = DenialForm()
    form2 = PollingPlaceFinder()

    form.electionId.choices = elections
    if form.validate_on_submit():
        denial = Denial(
                optPersonName=form2.optPersonName.data,
                optEmail=form2.optEmail.data,
                optPersonStreet=form2.optPersonStreet.data,
                optPersonCity=form2.optPersonCity.data,
                optPersonState=form2.optPersonState.data,
                optPersonZip=form2.optPersonZip.data,
                pollZip=form.pollZip.data,
                pollStreet=form.pollStreet.data,
                pollCity=form.pollCity.data,
                pollState=form.pollState.data,
                pollName=form.pollName.data,
                poc=form.poc.data,
                registration_type=form.registration_type.data,
                electionId=form.electionId.data)

        db.session.add(denial)
        db.session.commit()
        flash("Thanks for logging your denail...")
        return redirect(url_for('logged_denials'))
    post_state = utl.get_state_token()
    post_session['post_state'] = post_state
    page = request.args.get("page", 1, type=int)
    denials = Denial.query.order_by(Denial.timestamp.desc()).\
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    #  Pagination links
    next_url = url_for('denied', page=denials.next_num) \
        if denials.has_next else None
    prev_url = url_for('denied', page=denials.prev_num) \
        if denials.has_prev else None
    return render_template('denied.html', title="Log your denial",
                           form=form, form2=form2, denials=denials.items,
                           next_url=next_url, prev_url=prev_url,
                           elections=elections, POST_STATE=post_state)


@app.route('/polling_place', methods=['POST'])
def get_polling_place():
    """
    Try to find the polling place based on the personal address
    """
    response = utl.check_request(request.form['post_state'], post_session['post_state'])
    if response is not None:
        return response
    optPersonStreet = request.form['street']
    optPersonCity = request.form['city']
    optPersonState = request.form['state']
    optPersonZip = request.form['zip']
    address = "{},{},{} {},".format(
            optPersonStreet,
            optPersonCity,
            optPersonState,
            optPersonZip
        )

    electionId = request.form['electionId']
    response_data = jsonify(civic.get_polling_addresses(address, electionId))
    return response_data


@app.route('/logged_denials', methods=['GET'])
def logged_denials():
    page = request.args.get("page", 1, type=int)
    denials = Denial.query.order_by(Denial.timestamp.desc()).\
        paginate(page, app.config['POSTS_PER_PAGE'], False)
    #  Pagination links
    next_url = url_for('logged_denials', page=denials.next_num) \
        if denials.has_next else None
    prev_url = url_for('logged_denials', page=denials.prev_num) \
        if denials.has_prev else None
    return render_template(
            'logged_denials.html',
            title="List of logged denials",
            denials=denials.items,
            next_url=next_url, prev_url=prev_url,
        )