from collections import namedtuple

Database = namedtuple('Database', "value type uri")

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

clearDB_settings = Database(value=CLEARDB, type='mysql', uri=CLEARDB_URI)
