from collections import namedtuple
from os import environ

Database = namedtuple('Database', "type uri")

# MySQL Database Information
MYSQL_URI = 'mysql+mysqldb://root:root@localhost/citc_lab_dev'
mysql_settings  = Database(type='mysql', uri=MYSQL_URI)

# SQLite Database Information
SQLITE_URI = 'sqlite:///citc_lab_dev.db'
sqlite_settings = Database(type='sqlite', uri=SQLITE_URI)

# ClearDB MySQL Heroku Addon Database Information
if "CLEARDB_DATABASE_URL" in environ:
    CLEARDB_URI = environ["CLEARDB_DATABASE_URL"].split("?")[0]
    clearDB_settings = Database(type='mysql', uri=CLEARDB_URI)
