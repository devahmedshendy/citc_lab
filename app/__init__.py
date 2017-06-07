from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_cdn import CDN
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = 'this_is_my_secret_key'
app.config.from_object('config')

db  = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

assets = Environment(app)

from app import views, models

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
