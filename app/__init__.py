from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# for sending email
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
# email support
from flask_mail import Mail
# Deal with time in different regions
from flask_moment import Moment
# Flask Bootstrap for web page
from flask_bootstrap import Bootstrap
# for I18n and L10n (Language translation)
from flask_babel import Babel
from flask import request
from flask_babel import lazy_gettext as _l
# for current_app.config
from flask import current_app
# Full text research
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # When a blueprint is registered, any view functions,
    # templates, static files, error handlers, etc.
    # are connected to the application.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # For authentication, I thought it was nice to have all the routes
    # starting with /auth, so I added the prefix.
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # for api functions
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.main import bp as main_bp
    # app.register_blueprint(main_bp, url_prefix='/main')
    # Don't use url_prefix , or you will get a 404 in /
    app.register_blueprint(main_bp)

    # Integration of elasticsearch
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # Using SMTP to send email
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                secure = None
                if app.config['MAIL_USE_TLS']:
                    secure = ()
                mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                    credentials=auth, secure=secure
                )
                mail_handler.setLevel(logging.ERROR)
                app.logger.addHandler(mail_handler)
        # Logging file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


# module will define the structure of the database
from app import models


# app = Flask(__name__)
#
# # Add secret-key and other configurations
# app.config.from_object(Config)
#
# # db object represents the database
# db = SQLAlchemy(app)
#
# # migrate object represents the migration engine
# migrate = Migrate(app, db)
#
# # flask-login initialized
# login = LoginManager(app)
#
# # force login or the user will not view other pages
# login.login_view = 'login' # login url
# login.login_message = _l('Please log in to access this page.')
#
# # email support
# mail = Mail(app)
#
# # for web page
# bootstrap = Bootstrap(app)
#
# # timezone solution
# moment = Moment(app)
#
# # translation language
# babel = Babel(app)


#
# # The Babel instance provides a localeselector decorator.
# # The decorated function is invoked for each request to select
# # a language translation to use for that request.
# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(app.config['LANGUAGES'])
#
#
# # Using SMTP to send email
# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#             secure = None
#             if app.config['MAIL_USE_TLS']:
#                 secure = ()
#             mail_handler = SMTPHandler(
#                 mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#                 fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#                 toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#                 credentials=auth, secure=secure
#             )
#             mail_handler.setLevel(logging.ERROR)
#             app.logger.addHandler(mail_handler)
#     # Logging file
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Microblog startup')
#
# # When a blueprint is registered, any view functions,
# # templates, static files, error handlers, etc.
# # are connected to the application.
# from app.errors import bp as errors_bp
# app.register_blueprint(errors_bp)
#
# # For authentication, I thought it was nice to have all the routes
# # starting with /auth, so I added the prefix.
# from app.auth import bp as auth_bp
# app.register_blueprint(auth_bp, url_prefix='/auth')
#
# from app.main import bp as main_bp
# app.register_blueprint(main_bp, url_prefix='/main')
#
# # module will define the structure of the database
# from app import models
#
# # for 404 and 500 errors handling
# from app import errors
