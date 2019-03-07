"""
    Auth Services
"""
#pylint: disable=bad-whitespace
import uuid

from app.api import db

from app.api.models import User
from app.api.models import BlacklistToken

# exceptions
from sqlalchemy.exc import IntegrityError

from app.api.serializer import UserSchema

# http response
from app.api.http_response import created
from app.api.http_response import no_content
from app.api.http_response import ok

# exceptions
from app.api.error.http import *

# utility
from app.api.utility.utils import string_to_uuid

from app.config import config

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

ROLE = config.Config.ROLE
SECRET_KEY = config.Config.SECRET_KEY
TOKEN_CONFIG = config.Config.TOKEN_CONFIG
ERROR = config.Config.ERROR

class AuthServices:
    """ Auth Services Class"""

    def __init__(self, api, username):
        user = User.query.filter_by(api_id=api.id, username=username).first()
        if user is None:
            raise RequestNotFound(ERROR["USER_NOT_FOUND"]["TITLE"],
                                  ERROR["USER_NOT_FOUND"]["MESSAGE"])

        self.user = user

    def login(self, password):
        """ check username password"""
        if self.user.check_password(password) is False:
            raise Unauthorized(ERROR["INVALID_LOGIN"]["TITLE"],
                               ERROR["INVALID_LOGIN"]["MESSAGE"])

        token = self.generate_token()
        response = {"token" : token}
        return ok(response)
    #end def

    def generate_token(self):
        """ generate user token"""
        s = Serializer(SECRET_KEY, expires_in=TOKEN_CONFIG["EXPIRATION"])
        token = s.dumps({"id" : str(self.user.id)})
        return token.decode("utf-8")
    #end def

    @staticmethod
    def decode_token(token):
        s = Serializer(SECRET_KEY)
        try:
            payload = s.loads(token)
            blacklisted_status = BlacklistToken.is_blacklisted(token)
            if blacklisted_status:
                raise Unauthorized(ERROR["REVOKED_TOKEN"]["TITLE"],
                                   ERROR["REVOKED_TOKEN"]["MESSAGE"])
        except SignatureExpired:
            raise Unauthorized(ERROR["EXPIRED_TOKEN"]["TITLE"],
                               ERROR["EXPIRED_TOKEN"]["MESSAGE"])
        except BadSignature:
            raise Unauthorized(ERROR["BAD_SIGNATURE"]["TITLE"],
                               ERROR["BAD_SIGNATURE"]["MESSAGE"])
        user = User.query.get(payload["id"])
        return user
    #end def

    @staticmethod
    def revoke(token):
        """ blacklist a token"""
        blacklist = BlacklistToken(token=token)
        db.session.add(blacklist)
        db.session.commit()
        return no_content()
    #end def
