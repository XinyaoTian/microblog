# -*- encoding:utf-8 -*-
# 这个 routes.py 文件主要进行url与相应网页的 map 功能

from flask import render_template, flash, redirect, url_for
from app import app
from app import db

# These two moduels are imported for user login
from flask_login import current_user, login_user
from app.models import User

# for user logout
from flask_login import logout_user

# protection of pages from anonymous
from flask_login import login_required

# Redirect to "next" page after user login
from flask import request
from werkzeug.urls import url_parse

# for recording time last visited
from datetime import datetime

from app.forms import LoginForm
from app.forms import RegistrationForm


# @app.route('/')
# def hello():
#     user = {'username':'Daniel'}
#     return render_template('indexSmart.html', user=user)

# I can insert code that I want to execute
#  before any view function in the application
# by using the decorate @before_request
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user) # which is not necessary cause current user is already there
        db.session.commit()

@app.route('/index')
def index():
    user = {'username':'Winchester'}
    return render_template('index.html', title='Home', user=user)

@app.route('/loopEg')
def loopEg():
    comments_list = [
        {'author': 'Mike', 'body': 'Good day is today.'},
        {'author': 'Tim', 'body': 'Beijing is a beautiful city!'}
    ]

    user = {'username': 'Winchester'}

    return render_template('loopEg.html', user=user, comments=comments_list)

# Never Use Capital Letters in URLs ! No 'welcomePage' !
@app.route('/')
@app.route('/welcome')
@login_required
def welcome():
    # comments_list = [
    #     {'author': 'Mike', 'body': 'Good day is today.'},
    #     {'author': 'Tim', 'body': 'Beijing is a beautiful city!'}
    # ]
    #
    # user = {'username': 'Winchester'}
    posts = [
        {'author': 'Mike', 'body': 'Good day is today.'},
        {'author': 'Tim', 'body': 'Beijing is a beautiful city!'}
    ]

    return render_template('welcomePage.html', title='Home Page', posts=posts)

# a fake login function
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # the page will be redirect after login
        # Flask provides a request variable that contains
        # all the information that the client sent with the request.
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('welcome')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)