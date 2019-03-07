"""
    User Services
"""
#pylint: disable=bad-whitespace
import uuid

from app.api import db

from app.api.models import *

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
ERROR = config.Config.ERROR

class UserServices:
    """ User Services Class"""

    def __init__(self, user_id, candidate_id=None):
        user = User.query.filter_by(id=string_to_uuid(user_id), status=1).first()
        if user is None:
            raise RequestNotFound(ERROR["USER_NOT_FOUND"]["TITLE"],
                                  ERROR["USER_NOT_FOUND"]["MESSAGE"])
        #end if

        if candidate_id is not None:
            candidate_record = Candidate.query.filter_by(id=string_to_uuid(candidate_id), status=1).first()
            if candidate_record is None:
                raise RequestNotFound(ERROR["CANDIDATE_NOT_FOUND"]["TITLE"],
                                      ERROR["CANDIDATE_NOT_FOUND"]["MESSAGE"])

            self.candidate = candidate_record
        #end if
        self.user = user
    #end def

    @staticmethod
    def add(user, password):
        """ add user """
        try:
            # create uuid
            # assign foreign key
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise UnprocessableEntity(ERROR["DUPLICATE_USER"]["TITLE"],
                             ERROR["DUPLICATE_USER"]["MESSAGE"])
        #end try
        response = {
            "user_id" : str(user.id)
        }
        return created(response)
    #end def

    @staticmethod
    def show_all():
        """ add user """
        user = User.query.filter_by(status=1).all()
        user_list = UserSchema(many=True).dump(user).data
        return ok(user_list)
    #end def

    def info(self):
        """ get user info"""
        user_info = UserSchema().dump(self.user).data
        return {"data" : user_info}
    #end def

    def remove(self):
        """ remove user """
        db.session.delete(self.user)
        db.session.commit()
        return no_content()
    #end def

    def enroll(self):
        """ enroll user as candidate """
        self.user.candidate_id = self.candidate.id

        db.session.commit()
        return no_content()
    #end def

    def unroll(self):
        """ unroll user as candidate """
        self.user.candidate_id = None

        db.session.commit()
        return no_content()
    #end def

    def update(self, params):
        """ update user information """
        identity_id = params["identity_id"]
        msisdn      = params["msisdn"    ]
        email       = params["email"     ]
        role        = params["role"      ]
        name        = params["name"      ]
        password    = params["password"  ]

        self.user.name        = name
        self.user.identity_id = identity_id
        self.user.msisdn      = msisdn
        self.user.email       = email
        self.user.role        = ROLE[role]
        self.user.set_password(password)

        db.session.commit()
        return no_content()
    #end def
