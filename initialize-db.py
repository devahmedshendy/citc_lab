import MySQLdb
from app import db as application_db
from app import app
from app.models import User

#----
#
#
#
#### CONSTANTS ####
# Database Login Credentials
DB_HOST = app.config['DB_HOST']
DB_USER = app.config['DB_USER']
DB_PASSWD = app.config['DB_PASSWD']

# Master Branch Databse
DB_NAME = app.config['DB_NAME']

# Default Users
SUPER_USER = app.config['DEFAULT_SUPER_USER']
ADMIN      = app.config['DEFAULT_ADMIN']
DOCTOR     = app.config['DEFAULT_DOCTOR']
EMPLOYEE   = app.config['DEFAULT_EMPLOYEE']

# Theme Settings
STEP_CHAR = ">"
WARN_CHAR = "!"
ERR_CHAR  = "X"
STEP_DONE = "  DONE!."

#----
#
#
#
#### Functions ####
# Is for creating the database of the project
def create_database(cursor):
    print "{} Create database with name '{}'...".format(STEP_CHAR, DB_NAME)

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )

        print STEP_DONE

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error_no = list(e)[0]
        error_msg = list(e)[1]
        if error_no == 1007:
            print "{} Database <{}> already exists.".format(WARN_CHAR, DB_NAME)

        else:
            print "{} {}".format(ERR_CHAR, e)
            exit(1)

    except Exception as e:
        print e
        exit(1)

# Creating default table defined in app/models.py
def create_default_tables(db):
    print "{} Create application tables for '{}' database..." \
            .format(STEP_CHAR, DB_NAME)

    try:
        application_db.create_all()

        print STEP_DONE

    except Exception as e:
        print "{} {}".format(ERR_CHAR, e)
        application_db.session.rollback()
        exit(1)

# Defining default users whose username is as password
def create_default_user(firstname, lastname, username):
    print "{} Create default '{}' user..." \
            .format(STEP_CHAR, username)

    try:
        user = User()
        user.firstname = firstname
        user.lastname  = lastname
        user.username  = username
        user.hash_password(username)

        application_db.session.add(user)
        application_db.session.commit()

        print "  Username: {}".format(username)
        print "  Password: {}".format(username)
        print STEP_DONE

    except Exception as e:
        print "{} {}".format(ERR_CHAR, e.message)
        application_db.session.rollback()

#----
#
#
#
#### __main__ ####
script_cursor = MySQLdb.connect(host=DB_HOST, user=DB_USER,
                                passwd=DB_PASSWD).cursor()

create_database(script_cursor)
create_default_tables(application_db)

create_default_user(**SUPER_USER)

create_default_user(**ADMIN)
create_default_user(**DOCTOR)
create_default_user(**EMPLOYEE)

script_cursor.close()
