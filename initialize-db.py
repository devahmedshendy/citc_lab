# import MySQLdb, sqlite3
from urlparse import urlparse

from app import db as application_db
from app import app
from app.models import *
from app.constants import *

from config import db_settings

#--------------------------
#
# CONSTANTS
#--------------------------
# Default Users
ROOT     = { "firstname": "Super",
             "lastname": "User",
             "username": "superuser",
             "role_name": "root" }

ADMIN    = { "firstname": "Users",
             "lastname": "Admin",
             "username": "admin",
             "role_name": "admin" }

DOCTOR   = { "firstname": "Investigation",
             "lastname": "Doctor",
             "username": "doctor",
             "role_name": "doctor" }

OFFICER = { "firstname": "Registration",
             "lastname": "Officer",
             "username": "officer",
             "role_name": "officer" }

# Default Roles
ROOT_ROLE = ROLES["root"]
ADMIN_ROLE = ROLES["admin"]
DOCTOR_ROLE = ROLES["doctor"]
OFFICER_ROLE = ROLES["officer"]

# Default Roles/Users into an Array
DEFAULT_ROLES = [ ROLES["root"], ROLES["admin"],
                  ROLES["doctor"], ROLES["officer"] ]
DEFAULT_USERS = [ ROOT, ADMIN, DOCTOR, OFFICER]

# Output Theming
STEP_INFO   = ">"
STEP_WARN   = "!"
STEP_ERR    = "X"
STEP_DONE   = "  DONE!."

#--------------------------
#
# Functions
#--------------------------
def clear_database(db):
    print "{} Clear database...".format(STEP_INFO)

    try:
        db.drop_all()
        db.session.commit()

        print STEP_DONE

    except Exception as e:
        db.session.rollback()
        print "{} {}".format(STEP_ERR, e)
        exit(1)


def create_default_tables(db):
    clear_database(db)

    print "{} Create default tables...".format(STEP_INFO)

    try:
        db.drop_all()
        db.create_all()
        db.session.commit()

        print STEP_DONE

    except Exception as e:
        db.session.rollback()
        print "{} {}".format(STEP_ERR, e)
        exit(1)


def create_default_user(db, firstname, lastname, username, role_name):
    print "{} Create default '{}' user...".format(STEP_INFO, username)

    try:
        user = User()
        user.firstname = firstname
        user.lastname  = lastname
        user.username  = username
        user.hash_password(username)

        user.role_id = ROLES[role_name][0]

        db.session.add(user)
        db.session.commit()

        print "  Username: {}".format(username)
        print "  Password: {}".format(username)
        print STEP_DONE

    except Exception as e:
        db.session.rollback()
        print "{} {}".format(STEP_ERR, e.message)


def create_default_role(db, id, name):
    print "{} Create default '{}' role...".format(STEP_INFO, name)

    try:
        role = Role()
        role.id = id
        role.name = name

        db.session.add(role)
        db.session.commit()

        print "  Role Name: {}".format(name)
        print STEP_DONE

    except Exception as e:
        db.session.rollback()
        print "{} {}".format(STEP_ERR, e.message)

#--------------------------
#
# __main__
#--------------------------
create_default_tables(application_db)

for DEFAULT_ROLE in DEFAULT_ROLES:
    create_default_role(application_db, *DEFAULT_ROLE)

for DEFAULT_USER in DEFAULT_USERS:
    create_default_user(application_db, **DEFAULT_USER)
