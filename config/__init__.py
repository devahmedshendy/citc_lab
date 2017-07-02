from os.path import isfile
from os import environ

if isfile('app_config.py'):
    from app_config import app_config
else:
    from app_config_template import app_config

if isfile('db_config.py'):
    from db_config import mysql_settings, sqlite_settings, clearDB_settings
else:
    from db_config_template import mysql_settings, sqlite_settings, clearDB_settings


db_settings = sqlite_settings
app_config["DB_TYPE"] = db_settings.type
app_config["SQLALCHEMY_DATABASE_URI"] = db_settings.uri

if "CLEARDB_DATABASE_URL" in environ:
    db_settings = clearDB_settings
    app_config["DB_TYPE"] = db_settings.type
    app_config["SQLALCHEMY_DATABASE_URI"] = db_settings.uri

else:
    db_settings = sqlite_settings

app_config["DB_TYPE"] = db_settings.type
app_config["SQLALCHEMY_DATABASE_URI"] = db_settings.uri + '?reconnect=true'
