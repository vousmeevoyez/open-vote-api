"""
    Api Key Package Initialization
"""
from app.api.namespace import UserNamespace
api = UserNamespace.api 
from app.api.user import routes
