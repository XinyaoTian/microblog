# -*- encoding:utf-8 -*-
# 这个文件主要进行url与相应网页的 map 功能

from flask import render_template, flash, redirect, url_for
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
from app.forms import EditProfileForm

# post submission
from app.forms import PostForm
from app.models import Post

# password reset by email
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email

# I18n & L10n
from flask_babel import _

# for month and time translation
from flask import g
from flask_babel import get_locale

# for detecting language
from guess_language import guess_language

from flask import current_app
from app.main import bp


# I can insert code that I want to execute
#  before any view function in the application
# by using the decorate @before_request
@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user) # which is not necessary cause current user is already there
        db.session.commit()
    # for translate English month
    g.locale = str(get_locale())


# Never Use Capital Letters in URLs ! No 'welcomePage' !
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live'))
        return redirect(url_for('main.welcome'))
    page = request.args.get('page', 1, type=int)
    # posts = current_user.followed_posts().all()
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    # Go to next page or previous page
    next_url = url_for('main.welcome', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.welcome', page=posts.prev_num) \
        if posts.has_prev else None

    # The template receives the form object as an additional argument
    return render_template('welcomePage.html', title='Home Page',
                           form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


# a fake login function
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('welcome'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash(_('Invalid username or password'))
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         # the page will be redirect after login
#         # Flask provides a request variable that contains
#         # all the information that the client sent with the request.
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('welcome')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('welcome'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash(_('Congratulations, you are now a registered user!'))
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# # logout
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('welcome'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # prevent from reuse username
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash('User {} not found.'.format(username))
        # I18n & L10n
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.welcome'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    # flash('You are following {}!'.format(username))
    flash(_('You are following %(username)!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.welcome'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


# # password reset
# @app.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('welcome'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash('Check your email for the instructions to reset your password')
#         return redirect(url_for('login'))
#     return render_template('reset_password_request.html', title='Reset Password', form=form)


# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('welcome'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('welcome'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('login'))
#     return render_template('reset_password_request.html', form=form)


# explore view function
@bp.route('/explore')
@login_required
def explore():
    # Add pagination
    page = request.args.get('page', 1, type=int)
    # pagination function
    # change the '.all()' to '.pagination()' and return 'posts.items' instead of 'posts'
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('welcomePage.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
