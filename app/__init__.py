from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment
from flask_login import LoginManager
from flask_principal import Principal

from config import app_config

app = Flask(__name__)
app.secret_key = 'this_is_my_secret_key'
app.config.update(app_config)

db  = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

assets = Environment(app)

# load the extension
principals = Principal(app)


from app import views, models
from app.routes import users, patients, analyzes
