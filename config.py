import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Security token
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdef'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configurations for sending a email after some errors occur
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    ADMINS = ['leontian1024@gmail.com']

    # determines how many items will be displayed per page

    POSTS_PER_PAGE = 3

    # I18n & L10n
    LANGUAGES = ['en', 'es']

