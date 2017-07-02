from collections import namedtuple

Database = namedtuple('Database', "value type uri")

# MySQL Database Information
MYSQL_DB  = { "DRIVER"  : 'mysql+mysqldb',
              "NAME"    : 'citc_lab',
              "HOST"    : 'localhost',
              "USER"    : 'root',
              "PASSWD"  : 'root' }
MYSQL_URI = '{}://{}:{}@{}/{}'.format(MYSQL_DB["DRIVER"],
                                MYSQL_DB["USER"], MYSQL_DB["PASSWD"],
                                MYSQL_DB["HOST"], MYSQL_DB["NAME"])

# SQLite Database Information
SQLITE_DB  = {  "DRIVER"  : 'sqlite',
                "NAME"    : 'citc_lab_dev.db' }
SQLITE_URI = '{}:///{}'.format(SQLITE_DB["DRIVER"], SQLITE_DB["NAME"])

# ClearDB MySQL Heroku Addon Database Information
CLEARDB     = {  "DRIVER"  : 'mysql',
                 "NAME"    : 'citc_lab',
                 "HOST"    : 'us-cdbr-iron-east-03.cleardb.net',
                 "USER"    : 'bdbdf83b56d5d1',
                 "PASSWD"  : 'ae7444b9',
                 "OPTIONS" : 'reconnect=true' }
CLEARDB_URI = '{}://{}:{}@{}/{}?{}'.format(CLEARDB["DRIVER"],
                                CLEARDB["USER"], CLEARDB["PASSWD"],
                                CLEARDB["HOST"], CLEARDB["NAME"],
                                CLEARDB["OPTIONS"])


mysql_settings  = Database(value=MYSQL_DB, type='mysql', uri=MYSQL_URI)
sqlite_settings = Database(value=SQLITE_DB, type='sqlite', uri=SQLITE_URI)
clearDB_settings = Database(value=CLEARDB, type='mysql', uri=CLEARDB_URI)
