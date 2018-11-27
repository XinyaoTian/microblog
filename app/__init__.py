from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Add secert-key and other configurations
app.config.from_object(Config)

# db object represents the database
db = SQLAlchemy(app)

# migrate object represents the migration engine
migrate = Migrate(app, db)

# flask-login initialized
login = LoginManager(app)

# force login or the user will not view other pages
login.login_view = 'login' # login url

from app import routes

# module will define the structure of the database
from app import models