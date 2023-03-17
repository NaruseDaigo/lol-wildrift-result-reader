from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True

db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

from app import routes, models