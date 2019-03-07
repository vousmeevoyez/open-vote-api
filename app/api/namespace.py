""" 
    Flask Restplus Namespace
"""
from flask_restplus import Namespace

class ApiKeyNamespace:
    api = Namespace("api_key")
#end class

class UserNamespace:
    api = Namespace("user")
#end class

class OauthNamespace:
    api = Namespace("oauth")
#end class

class ElectionNamespace:
    api = Namespace("election")
#end class

class StaticNamespace:
    api = Namespace("static")
#end class
