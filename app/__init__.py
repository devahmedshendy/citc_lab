from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_cdn import CDN

app = Flask(__name__)

app.secret_key = 'this_is_my_secret_key'
app.config.from_object('config')

db  = SQLAlchemy(app)
assets = Environment(app)

from app import views, models
