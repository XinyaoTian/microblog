from flask import Flask
from config import Config

app = Flask(__name__)
# Add secert-key
app.config.from_object(Config)

from app import routes