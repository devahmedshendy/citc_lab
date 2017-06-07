from app import app, db

from datetime import datetime
from bcrypt import hashpw, gensalt


class User(db.Model):
    __tablename__ = 'users'

    # Colunmns map
    id               = db.Column(db.Integer, primary_key=True)
    firstname        = db.Column(db.String(45))
    lastname         = db.Column(db.String(45))
    username         = db.Column(db.String(45), unique=True)
    hashed_password  = db.Column(db.String(160))
    created_at       = db.Column(db.DateTime)
    updated_at       = db.Column(db.DateTime)

    authenticated    = False


    def __init__(self, firstname=None, lastname=None, username=None, password=None):
        self.firstname = firstname
        self.lastname  = lastname
        self.username = username
        self.hashed_password = User.hash_password(password)
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


    @staticmethod
    def hash_password(password):
        return hashpw(password, gensalt())


    @staticmethod
    def verify_password(password, hashed_password):
        return hashed_password == hashpw(password, hashed_password)


    def __repr__(self):
        return '<User %r %r>' % (self.firstname, self.lastname)


class Patient(db.Model):
    __tablename__ = 'patients'

    # Colunmns map
    id          = db.Column(db.Integer, primary_key=True)
    personal_id = db.Column(db.String(14), unique=True)
    name        = db.Column(db.String(45))
    address     = db.Column(db.String(45))
    phone       = db.Column(db.Integer)
    age         = db.Column(db.Integer)
    gender      = db.Column(db.String(45))
    created_at  = db.Column(db.DateTime)
    updated_at  = db.Column(db.DateTime)


    def __init__(self, personal_id, name, address, phone, age, gender):
        self.personal_id    = personal_id
        self.name           = name
        self.address        = address
        self.phone          = phone if phone else 0
        self.age            = age
        self.gender         = gender
        self.created_at     = datetime.now()
        self.updated_at     = datetime.now()

    def serialize(self):
        return {
            'personal_id': self.personal_id,
            'name': self.name,
            'address': self.phone,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender
        }
