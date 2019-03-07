""" 
    HTTP Response
    __________
    This module to handle HTTP Success & Error code
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
"""
    2xx Success
"""
def no_content():
    """
        Function to return 204 HTTP success message
    """
    return ('', 204)
#end def

def ok(data=None, message=None):
    """
        Function to return 200 HTTP success message
    """
    response = {}

    if data is not None:
        response["data"] = data

    if message is not None:
        response["message"] = message

    return (response, 200)
#end def

def created(data=None, message=None):
    """
        Function to return 201 HTTP success message
    """
    response = {}

    if data is not None:
        response["data"] = data

    if message is not None:
        response["message"] = message

    return (response, 201)
#end def

def accepted(message=None):
    """
        Function to return 202 HTTP success message
    """
    response = {}

    if message is not None:
        response["message"] = message

    return (response, 202)
#end def
