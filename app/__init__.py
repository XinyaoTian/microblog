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

app = Flask(__name__)

# Add secret-key and other configurations
app.config.from_object(Config)

# db object represents the database
db = SQLAlchemy(app)

# migrate object represents the migration engine
migrate = Migrate(app, db)

# flask-login initialized
login = LoginManager(app)

# force login or the user will not view other pages
login.login_view = 'login' # login url

# email support
mail = Mail(app)

# Using SMTP to send email
if not app.debug:
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


from app import routes

# module will define the structure of the database
from app import models

# for 404 and 500 errors handling
from app import errors
