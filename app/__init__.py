from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment
from flask_login import LoginManager

from config import app_config

app = Flask(__name__)
app.secret_key = 'this_is_my_secret_key'
app.config.update(app_config)

db  = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

assets = Environment(app)

from app import views, models

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
