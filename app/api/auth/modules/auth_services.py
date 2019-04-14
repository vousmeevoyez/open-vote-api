"""
   Auth Services
"""
#pylint: disable=bad-whitespace
from app.api import db

# models
from app.api.models import *

# exceptions
from sqlalchemy.exc import IntegrityError

# http response
from app.api.http_response import created
from app.api.http_response import no_content
from app.api.http_response import ok

# sechema
from app.api.serializer import UserSchema

# exceptions
from app.api.error.http import *
from app.api.error.token import *

from app.config import config

from app.api.utility.utils import string_to_uuid

ERROR = config.Config.ERROR

class AuthServices:
    """ Candidate Services Class"""

    def __init__(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise RequestNotFound(ERROR["USER_NOT_FOUND"]["TITLE"],
                                  ERROR["USER_NOT_FOUND"]["MESSAGE"])
        self._user = user
    #end def

    def login(self, password):
        """ check username password here"""
        if self._user.check_password(password) is False:
            raise Unauthorized(ERROR["INVALID_LOGIN"]["TITLE"],
                               ERROR["INVALID_LOGIN"]["MESSAGE"])

        if self._user.role == 0:
            role = "SUPERADMIN"
        elif self._user.role == 1:
            role = "ADMIN"
        elif self._user.role == 2:
            role = "COMMITEE"
        elif self._user.role == 3:
            role = "PARTICIPANT"

        access_token = User.encode_token("ACCESS", self._user.id, role).decode()
        #user_info = UserSchema().dump(self._user).data
        #return ok({"access_token" : access_token, "user": user_info})
        return ok({"access_token" : access_token})
    #end def

    @staticmethod
    def logout(token):
        """" revoke thte user token"""
        blacklist = BlacklistToken(token=token)
        try:
            db.session.add(blacklist)
            db.session.commit()
        except IntegrityError:
            print("here")
            db.session.rollback()

        return no_content()
    #end def

    @staticmethod
    def _current_login_user(token):
        """
            function to check who is currently login by decode their token
            used in decorator
            args:
                token -- jwt token
        """
        try:
            payload = User.decode_token(token)
        except RevokedTokenError:
            raise Unauthorized(ERROR["REVOKED_TOKEN"]["TITLE"],
                               ERROR["REVOKED_TOKEN"]["MESSAGE"])
        except SignatureExpiredError as error:
            #print(error)
            raise Unauthorized(ERROR["SIGNATURE_EXPIRED"]["TITLE"],
                               ERROR["SIGNATURE_EXPIRED"]["MESSAGE"])
        except InvalidTokenError as error:
            #print(error)
            raise BadRequest(ERROR["INVALID_TOKEN"]["TITLE"],
                             ERROR["INVALID_TOKEN"]["MESSAGE"])
        except EmptyPayloadError:
            raise Unauthorized(ERROR["EMPTY_PAYLOAD"]["TITLE"],
                               ERROR["EMPTY_PAYLOAD"]["MESSAGE"])

        response = {
            "token_type": payload["type"],
            "user_id"   : payload["sub"],
            "role"      : payload["role"],
        }
        return response
    #end def
