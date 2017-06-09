from app import app, db

from datetime import datetime
from bcrypt import hashpw, gensalt


class User(db.Model):
    __tablename__ = 'users'

    # Columns map
    id               = db.Column(db.Integer, primary_key=True)
    firstname        = db.Column(db.String(45))
    lastname         = db.Column(db.String(45))
    username         = db.Column(db.String(45), unique=True)
    hashed_password  = db.Column(db.String(160))
    created_at       = db.Column(db.DateTime)
    updated_at       = db.Column(db.DateTime)

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


    # @staticmethod
    def hash_password(self, password):
        self.hashed_password = hashpw(password, gensalt())


    @staticmethod
    def verify_password(password, hashed_password):
        return hashed_password == hashpw(password, hashed_password)


    def __repr__(self):
        return '<User %r %r>' % (self.firstname, self.lastname)


class Patient(db.Model):
    __tablename__ = 'patients'

    # Columns map
    id            = db.Column(db.Integer, primary_key=True)
    personal_id   = db.Column(db.String(14), unique=True)
    name          = db.Column(db.String(45))
    address       = db.Column(db.String(45))
    phone         = db.Column(db.String(12))
    age           = db.Column(db.String(3))
    gender        = db.Column(db.String(45))
    created_at    = db.Column(db.DateTime)
    updated_at    = db.Column(db.DateTime)
    cbc_analyzes  = db.relationship('CBCAnalysis', backref='patient', lazy='dynamic')


    def __init__(self):
        self.created_at     = datetime.now()
        self.updated_at     = datetime.now()


class CBCAnalysis(db.Model):
    __tablename__ = 'cbc_analysis'

    id          = db.Column(db.Integer, primary_key=True)
    WCB         = db.Column(db.String(45))
    HGB         = db.Column(db.String(45))
    MCV         = db.Column(db.String(45))
    MCH         = db.Column(db.String(45))
    comment     = db.Column(db.String(45))
    created_at  = db.Column(db.DATETIME)
    updated_at  = db.Column(db.DATETIME)
    type_id     = db.Column(db.Integer, db.ForeignKey('analysis_types.id'))
    patient_id  = db.Column(db.Integer, db.ForeignKey('patients.id'))

    def __init__(self, wcb, hgb, mcv, mch, comment, type_id, patient_id, created_at=None, updated_at=None):
        self.WCB            = wcb
        self.HGB            = hgb
        self.MCV            = mcv
        self.MCH            = mch
        self.comment        = comment
        self.updated_at     = updated_at
        self.type_id        = type_id
        self.patient_id     = patient_id
        self.created_at = datetime.now() if created_at == None else created_at
        self.updated_at = datetime.now() if updated_at == None else updated_at


class AnalysisType(db.Model):
    __tablename__ = 'analysis_types'

    id          = db.Column(db.Integer, primary_key=True)
    type        = db.Column(db.String(45))
    cbc_analyzes    = db.relationship('CBCAnalysis', backref='analysis_type', lazy='dynamic')
