"""
    Main Model
    _____________
"""
#pylint: disable=no-member
import uuid
import jwt

from datetime import datetime
from datetime import timedelta

from sqlalchemy.dialects.postgresql import UUID

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app.api import db
from app.config import config

from app.api.error.token import *

now = datetime.utcnow()

JWT_CONFIG = config.Config.JWT_CONFIG

def generate_uuid():
    return uuid.uuid4()

class User(db.Model):
    """
        this is class that represent User Table
    """
    id          = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=generate_uuid)
    username    = db.Column(db.String(144), unique=True)
    identity_id = db.Column(db.String(144), unique=True)
    name        = db.Column(db.String(144))
    msisdn      = db.Column(db.String(12), unique=True)
    email       = db.Column(db.String(144), unique=True)
    images      = db.Column(db.String(144))
    created_at  = db.Column(db.DateTime, default=now) # UTC
    password    = db.Column(db.String(128)) # hashed password
    status      = db.Column(db.Integer, default=1) # active / deactive
    role        = db.Column(db.Integer, default=3)
    candidate_id= db.Column(UUID(as_uuid=True), db.ForeignKey("candidate.id"))
    candidate   = db.relationship("Candidate", back_populates="users") # many to
    vote        = db.relationship("Vote", back_populates="user")

    def __repr__(self):
        return '<User {} {} {} {}>'.format(self.id, self.username,
                                           self.role, self.status)

    def set_password(self, password):
        """
            Function to set hashed password
            args :
                password -- password
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
            Function to check hashed password
            args :
                password -- password
        """
        return check_password_hash(self.password, password)

    @staticmethod
    def encode_token(token_type, user_id, role):
        """
            Function to create JWT Token
            args :
                token_type -- Access / Refresh
                user_id -- User identity
                role -- User Role
        """
        if token_type == "ACCESS":
            exp = datetime.utcnow() + timedelta(minutes=JWT_CONFIG["EXPIRE"])
        elif token_type == "REFRESH":
            exp = datetime.utcnow() + timedelta(days=JWT_CONFIG["EXPIRE"])

        payload = {
            "exp" : exp,
            "iat" : datetime.utcnow(),
            "sub" : str(user_id),
            "type": token_type,
            "role" : role
        }
        return jwt.encode(
            payload,
            JWT_CONFIG["SECRET"],
            JWT_CONFIG["ALGORITHM"]
        )

    @staticmethod
    def decode_token(token):
        """
            Function to decode JWT Token
            args :
                token -- Jwt token
        """
        try:
            payload = jwt.decode(token, JWT_CONFIG["SECRET"],
                                 algorithms=JWT_CONFIG["ALGORITHM"])
            blacklist_status = BlacklistToken.is_blacklisted(token)
            if blacklist_status:
                raise RevokedTokenError
            if not payload:
                raise EmptyPayloadError
        except jwt.ExpiredSignatureError as error:
            raise SignatureExpiredError(error)
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError(error)
        return payload

class Election(db.Model):
    """
        this is class that represent Election Table
    """
    id          = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=generate_uuid)
    name        = db.Column(db.String(144))
    images      = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at  = db.Column(db.DateTime, default=now) # UTC
    status      = db.Column(db.Integer, default=1) # ACTIVE / DEACTIVE
    candidates  = db.relationship("Candidate", back_populates="election")#1ton

    def __repr__(self):
        return '<Election {} {} {} {}>'.format(self.id, self.name,
                                               self.images, self.description)

class Candidate(db.Model):
    """
        this is class that represent Candidate Table
    """
    id          = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=generate_uuid)
    name        = db.Column(db.String(144))
    description = db.Column(db.String(255))
    images      = db.Column(db.String(255))
    created_at  = db.Column(db.DateTime, default=now) # UTC
    status      = db.Column(db.Integer, default=1) # ACTIVE / DEACTIVE
    election_id = db.Column(UUID(as_uuid=True), db.ForeignKey("election.id"))
    election    = db.relationship("Election", back_populates="candidates") # many to
    votes       = db.relationship("Vote", back_populates="candidate") # 1 to 1
    users       = db.relationship("User", back_populates="candidate") # 1 to 1

    def __repr__(self):
        return '<Candidate  {} {} {} {}>'.format(self.id, self.name,
                                                    self.images, self.description, self.election_id)

class Vote(db.Model):
    """
        this is class that represent Voting Table
    """
    id          = db.Column(UUID(as_uuid=True), unique=True, primary_key=True, default=generate_uuid)
    candidate_id= db.Column(UUID(as_uuid=True), db.ForeignKey("candidate.id"))
    candidate   = db.relationship("Candidate", back_populates="votes") # 1 to 1
    user_id     = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"))
    user        = db.relationship("User", back_populates="vote") # 1 to 1
    created_at  = db.Column(db.DateTime, default=now) # UTC

class BlacklistToken(db.Model):
    """
        This is class Model for Blacklisted Token
    """
    id          = db.Column(db.Integer, primary_key=True)
    token       = db.Column(db.String(255))
    created_at  = db.Column(db.DateTime, default=now)

    @staticmethod
    def is_blacklisted(token):
        """
            function to check whether token has been blacklisted or not
            args :
                token -- JWT Token
        """
        result = BlacklistToken.query.filter_by(token=token).first()
        return bool(result)

    def __repr__(self):
        return '<Blacklist Token {} {}>'.format(self.id, self.jti)
    #end def
#end class
