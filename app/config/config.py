"""
    Configuration
    _______________
    This is module for storing all configuration for various environments
"""
import os

basedir = os.path.abspath(os.path.dirname("data"))

class Config:
    """ This is base class for configuration """
    DEBUG = False

    UPLOAD_FOLDER = basedir + "/data/images/"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    DATABASE = {
        "DRIVER"   : os.getenv('DB_DRIVER') or "postgresql://", # sqlite // postgresql // mysql
        "USERNAME" : os.getenv('DB_USERNAME') or "evote",
        "PASSWORD" : os.getenv('DB_PASSWORD') or "passsword",
        "HOST_NAME": os.getenv('DB_HOSTNAME') or "localhost",
        "DB_NAME"  : os.getenv('DB_NAME') or "db_evote",
    }

    SENTRY_CONFIG = {}

    ROLE = {
        "SUPERADMIN" : 0,
        "ADMIN"      : 1,
        "COMMITEE"   : 2,
        "PARTICIPANT": 3,
    }

    JWT_CONFIG = {
        "EXPIRE" : 3600,
        "SECRET" : os.getenv('JWT_SECRET') or "somekajsdljashdhaskldhkjahskjdhkjashkjdhaksjhjdkhaskh",
        "ALGORITHM" : "HS256",
    }

    ERROR = {
        "ADMIN_REQUIRED" : {
            "TITLE"   : "ADMIN_REQUIRED",
            "MESSAGE" : "Require Admin Permission",
        },
        "DECODE" : {
            "TITLE"   : "INVALID_KEY",
            "MESSAGE" : "Failed decode key",
        },
        "REVOKED_TOKEN" : {
            "TITLE"   : "REVOKED_TOKEN",
            "MESSAGE" : "Token has been revoked",
        },
        "SIGNATURE_EXPIRED" : {
            "TITLE"   : "EXPIRED_TOKEN",
            "MESSAGE" : "Token has expired",
        },
        "BAD_SIGNATURE" : {
            "TITLE"   : "BAD_SIGNATURE",
            "MESSAGE" : "Bad Signature",
        },
        "BAD_AUTH_HEADER" : {
            "TITLE"   : "BAD_SIGNATURE",
        },
        "INVALID_TOKEN" : {
            "TITLE"   : "INVALID_TOKEN",
            "MESSAGE" : "Invalid Token",
        },
        "EMPTY_PAYLOAD" : {
            "TITLE"   : "EMPTY_PAYLOAD",
            "MESSAGE" : "Empty Token Payload",
        },
        "INVALID_LOGIN" : {
            "TITLE"   : "INVALID_LOGIN",
            "MESSAGE" : "Invalid Username/Password",
        },
        "API_KEY_NOT_FOUND" : {
            "TITLE"   : "API_KEY_NOT_FOUND",
            "MESSAGE" : "Api Key not Found",
        },
        "USER_NOT_FOUND" : {
            "TITLE"   : "USER_NOT_FOUND",
            "MESSAGE" : "User not Found",
        },
        "INVALID_PARAMETER" : {
            "TITLE"   : "INVALID_PARAMETER",
            "MESSAGE" : "Invalid Parameter",
        },
        "INVALID_API_KEY" : {
            "TITLE"   : "INVALID_API_KEY",
        },
        "ALREADY_VOTE" : {
            "TITLE"   : "ALREADY_VOTE",
            "MESSAGE" : "User already vote",
        },
        "DUPLICATE_API_KEY" : {
            "TITLE"   : "DUPLICATE_API_KEY",
            "MESSAGE" : "Api key already exist",
        },
        "DUPLICATE_USER" : {
            "TITLE"   : "DUPLICATE_USER",
            "MESSAGE" : "User already exist",
        },
        "USER_NOT_FOUND" : {
            "TITLE"   : "USER_NOT_FOUND",
            "MESSAGE" : "User not Found",
        },
        "ELECTION_NOT_FOUND" : {
            "TITLE"   : "ELECTION_NOT_FOUND",
            "MESSAGE" : "Election not Found",
        },
        "CANDIDATE_NOT_FOUND" : {
            "TITLE"   : "CANDIDATE_NOT_FOUND",
            "MESSAGE" : "Candidate not Found",
        },
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # FLASK RESTPLUS
    ERROR_INCLUDE_MESSAGE = False
#end class


class DevelopmentConfig(Config):
    """ This is class for development configuration """
    DEBUG = True

    DATABASE = Config.DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
            DATABASE["DRIVER"] + DATABASE["USERNAME"] + ":" + \
            DATABASE["PASSWORD"] + "@" + DATABASE["HOST_NAME"] + "/" + \
            DATABASE["DB_NAME"] + "_dev"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
#end class


class TestingConfig(Config):
    """ This is class for testing configuration """
    DEBUG = True
    TESTING = True

    DATABASE = Config.DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
            DATABASE["DRIVER"] + DATABASE["USERNAME"] + ":" + \
            DATABASE["PASSWORD"] + "@" + DATABASE["HOST_NAME"] + "/" + \
            DATABASE["DB_NAME"] + "_testing"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENTRY_CONFIG = {}
#end class


class ProductionConfig(Config):
    """ This is class for production configuration """
    DEBUG = False

    DATABASE = Config.DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
            DATABASE["DRIVER"] + DATABASE["USERNAME"] + ":" + \
            DATABASE["PASSWORD"] + "@" + DATABASE["HOST_NAME"] + "/" + \
            DATABASE["DB_NAME"] + "_prod"
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SENTRY_CONFIG = Config.SENTRY_CONFIG
    SENTRY_CONFIG["dsn"] = os.environ.get("SENTRY_DSN")
#end class

CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
