"""
    Auth Package Initialization
"""
from app.api.namespace import OauthNamespace
api = OauthNamespace.api 
from app.api.oauth import oauth2, routes
