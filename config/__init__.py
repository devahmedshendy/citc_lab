from os.path import isfile

if isfile('app_config.py'):
    from app_config import app_config
else:
    from app_config_template import app_config

if isfile('db_config.py'):
    from db_config import mysql_settings, sqlite_settings
else:
    from db_config_template import mysql_settings, sqlite_settings


db_settings = mysql_settings
app_config["DB_TYPE"] = db_settings.type
app_config["SQLALCHEMY_DATABASE_URI"] = db_settings.uri
