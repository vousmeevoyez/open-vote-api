"""
    Flask App
    ______________________
    Package Initialization
"""
from flask  import Flask

from flask_sqlalchemy   import SQLAlchemy
from flask_marshmallow  import Marshmallow
from flask_oauthlib.provider import OAuth2Provider

from raven.contrib.flask import Sentry

from werkzeug.contrib.fixers import ProxyFix

from app.config import config

db = SQLAlchemy()
ma = Marshmallow()
sentry = Sentry()
auth = OAuth2Provider()

def create_app(config_name):
    """
        Create flask instance using application factory pattern

        args :
            config_name -- Configuration key used (DEV/PROD/TESTING)
    """
    app = Flask(__name__)
    app.config.from_object(config.CONFIG_BY_NAME[config_name])

    app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(app)
    ma.init_app(app)
    auth.init_app(app)

    if not app.debug and not app.testing:
        sentry.init_app(app)

    return app