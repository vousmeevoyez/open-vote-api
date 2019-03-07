"""
   Election Package Initialization
"""
from app.api.namespace import ElectionNamespace
api = ElectionNamespace.api 
from app.api.election import routes
