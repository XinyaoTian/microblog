from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Add secert-key
app.config.from_object(Config)

# db object represents the database
db = SQLAlchemy(app)

# migrate object represents the migration engine
migrate = Migrate(app, db)

from app import routes

# module will define the structure of the database
from app import models