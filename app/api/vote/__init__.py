"""
    Vote Package Initialization
"""
from app.api.namespace import VoteNamespace
api = VoteNamespace.api 
from app.api.vote import routes
