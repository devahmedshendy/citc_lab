# Database Information
DB_NAME     = 'citc_lab_dev'
DB_DRIVER   = 'mysql+mysqldb'
DB_HOST     = 'localhost'
DB_USER     = 'root'
DB_PASSWD   = 'root'

# Default Users
DEFAULT_SUPER_USER  = { "firstname": "Super",
                        "lastname": "User",
                        "username": "superuser"}
DEFAULT_ADMIN       = { "firstname": "Admin",
                        "lastname": "User",
                        "username": "admin"}
DEFAULT_DOCTOR      = { "firstname": "Investigation",
                        "lastname": "Doctor",
                        "username": "doctor"}
DEFAULT_EMPLOYEE    = { "firstname": "Registeration",
                        "lastname": "Employee",
                        "username": "emp"}

# Application Configuration
WTF_CSRF_ENABLED = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'.format(
                            DB_DRIVER, DB_USER, DB_PASSWD, DB_HOST, DB_NAME)
