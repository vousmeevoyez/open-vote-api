"""
    Auth Routes
"""
from flask_restplus import Resource

from marshmallow import ValidationError

from app.api.auth import api
from app.api.request_schema import *
from app.api.serializer import UserSchema
# services
from app.api.auth.modules.auth_services import AuthServices
# exception
from app.api.error.http import *
# decorators
from app.api.auth.decorators import *

from app.config import config

ERROR = config.Config.ERROR

auth_request_schema = AuthRequestSchema.parser

@api.route("/login")
class UserRoutes(Resource):
    """
        User routes
        api/v1/auth/login
    """
    def post(self):
        """
            handle post request
            Add User
        """
        request_data = auth_request_schema.parse_args(strict=True)
        try:
            excluded = "name", "identity_id", "msisdn", "email"
            user = UserSchema().validate(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try
        response = AuthServices(request_data["username"]).login(request_data["password"])
        return response

@api.route("/logout")
class UserRoutes(Resource):
    """
        User routes
        api/v1/auth/logout
    """
    @token_required
    def post(self):
        """
            handle post request
            Add User
        """
        token = get_current_token()
        response = AuthServices.logout(token)
        return response
