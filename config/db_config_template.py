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


mysql_settings  = Database(value=MYSQL_DB, type='mysql', uri=MYSQL_URI)
sqlite_settings = Database(value=SQLITE_DB, type='sqlite', uri=SQLITE_URI)
