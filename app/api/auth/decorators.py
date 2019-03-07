"""
    Auth Decorator
    ________________
    this is module that contain various decorator to protect various endpoint
"""
from functools import wraps
from flask import request

from flask_restplus import reqparse

from app.api.auth.modules.auth_services import AuthServices

from app.api.models import User

from app.api.error.http import *

from app.config import config

ERROR = config.Config.ERROR

class ParseError(Exception):
    """ raised when failed parsing token from header"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def _parse_token():
    """ parse token from header """
    parser = reqparse.RequestParser()
    parser.add_argument('Authorization', location='headers', required=True)
    header = parser.parse_args()

    # accessing token from header
    auth_header = header["Authorization"]
    if auth_header == "":
        raise ParseError("Empty Auth Header")
    #end if

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise ParseError("Invalid Auth Header")
    #end def
    return token
#end def

def get_token_payload():
    """ get token payload """
    # define header schema

    try:
        token = _parse_token()
    except ParseError as error:
        raise BadRequest(ERROR["BAD_AUTH_HEADER"], error.message)
    #end def

    response = AuthServices._current_login_user(token)
    return response
#end def

# CUSTOM DECORATOR
def admin_required(fn):
    """
        decorator to only allow admin access this function
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):

        response = get_token_payload()
        # check permission here
        if response['role'] not in ["SUPERADMIN","ADMIN"] :
            raise InsufficientScope(ERROR["ADMIN_REQUIRED"]["TITLE"],
                                    ERROR["ADMIN_REQUIRED"]["MESSAGE"])

        return fn(*args, **kwargs)
        #end if
    return wrapper
#end def

def token_required(fn):
    """
        protect routes with token
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):

        response = get_token_payload()

        return fn(*args, **kwargs)
    return wrapper
#end def

def get_current_token():
    """ get current token from headers """
    # define header schema
    try:
        token = _parse_token()
    except ParseError as error:
        raise BadRequest(ERROR["BAD_AUTH_HEADER"], error.message)
    #end def
    return token
#end def
