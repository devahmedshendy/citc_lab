from app import app, db
from flask_login import UserMixin
# from app.db import Table, Column, Integer, String, DateTime, ForeignKey, relationship

from datetime import datetime
from bcrypt import hashpw, gensalt

from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql import expression



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Columns map
    id               = db.Column(db.Integer, primary_key=True)
    firstname        = db.Column(db.String(45))
    lastname         = db.Column(db.String(45))
    username         = db.Column(db.String(45), unique=True)
    hashed_password  = db.Column(db.String(160))
    created_at       = db.Column(db.DateTime)
    updated_at       = db.Column(db.DateTime)
    role_id          = db.Column('role_id', db.ForeignKey('roles.id'), nullable=False)

    authenticated    = False


    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def is_authenticated(self):
        return authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def hash_password(self, password):
        self.hashed_password = hashpw(password, gensalt())


    @staticmethod
    def verify_password(password, hashed_password):
        return hashed_password == hashpw(password, hashed_password)


    def __repr__(self):
        return 'User: %s %s' % (self.firstname, self.lastname)



class Role(db.Model):
    __tablename__ = 'roles'

    # Columns map
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(45), unique=True)

    users         = db.relationship("User",
                                    backref="role",
                                    lazy="dynamic")



class Patient(db.Model):
    __tablename__ = 'patients'

    # Columns map
    id            = db.Column(db.Integer, primary_key=True)
    personal_id   = db.Column(db.String(14), unique=True)
    name          = db.Column(db.String(45))
    address       = db.Column(db.String(45))
    phone         = db.Column(db.String(13))
    # phone         = db.Column(BIGINT(unsigned=True))
    age           = db.Column(db.String(3))
    gender        = db.Column(db.String(45))
    created_at    = db.Column(db.DateTime)
    updated_at    = db.Column(db.DateTime)

    # Join Relationship Map
    cbc_analyzes  = db.relationship('CBCAnalysis', \
                                    backref='patient', \
                                    lazy='dynamic', \
                                    cascade='all, delete-orphan')

    def __init__(self):
        self.created_at     = datetime.now()
        self.updated_at     = datetime.now()


    def __repr__(self):
        return "Patient: %s" % (self.name)


class CBCAnalysis(db.Model):
    __tablename__ = 'cbc_analysis'

    id              = db.Column(db.Integer, primary_key=True)
    WCB             = db.Column(db.String(45))
    HGB             = db.Column(db.String(45))
    MCV             = db.Column(db.String(45))
    MCH             = db.Column(db.String(45))
    comment         = db.Column(db.String(200))
    comment_doctor  = db.Column(db.String(45))
    created_at      = db.Column(db.DateTime)
    updated_at      = db.Column(db.DateTime)
    approved        = db.Column(db.Boolean, server_default=expression.false(), default=False, nullable=False)
    approved_at     = db.Column(db.DateTime)

    # Join Relationship Map
    patient_id  = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, wcb, hgb, mcv, mch, type_id, patient_id, comment=None, comment_doctor=None):
        self.WCB            = wcb
        self.HGB            = hgb
        self.MCV            = mcv
        self.MCH            = mch
        self.created_at     = datetime.now()
        self.updated_at     = datetime.now()
        self.type_id        = type_id
        self.patient_id     = patient_id
        if comment_doctor == None or len(comment_doctor) == 0:
            self.comment    = 'No Comment Yet.'
        else:
            self.comment        = comment
            self.comment_doctor = comment_doctor

    def serialize(self):
        if self.approved:
            return {
                "id"                : self.id,
                "WCB"               : self.WCB,
                "HGB"               : self.HGB,
                "MCV"               : self.MCV,
                "MCH"               : self.MCH,
                "comment"           : self.comment,
                "comment_doctor"    : self.comment_doctor,
                "approved"          : self.approved,
                "approved_at"       : self.approved_at.strftime("%Y-%m-%d"),
                "updated_at"        : self.updated_at.strftime("%b %d, %Y - %I:%M %p"),
            }

        else:
            return {
                "id"                : self.id,
                "WCB"               : self.WCB,
                "HGB"               : self.HGB,
                "MCV"               : self.MCV,
                "MCH"               : self.MCH,
                "comment"           : self.comment,
                "comment_doctor"    : self.comment_doctor,
                "approved"          : self.approved,
                "updated_at"        : self.updated_at.strftime("%b %d, %Y - %I:%M %p"),
            }

    def approve(self):
        self.approved = True
        self.approved_at = datetime.now()


    def __repr__(self):
        return "CBC: %s" % (self.id)
