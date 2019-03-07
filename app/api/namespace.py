""" 
    Flask Restplus Namespace
"""
from flask_restplus import Namespace

class UserNamespace:
    api = Namespace("user")
#end class

class AuthNamespace:
    api = Namespace("auth")
#end class

class ElectionNamespace:
    api = Namespace("election")
#end class

class StaticNamespace:
    api = Namespace("static")
#end class

class VoteNamespace:
    api = Namespace("vote")
#end class
