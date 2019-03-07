"""
    User Routes
"""
from flask_restplus import Resource

from marshmallow import ValidationError

from app.api.user import api

# flask rest plus extesnion
from app.api.request_schema import *
from app.api.serializer import UserSchema
# services
from app.api.user.modules.user_services import UserServices
# exception
from app.api.error.http import *
# decorator
from app.api.auth.decorators import admin_required

from app.config import config

ERROR = config.Config.ERROR

request_schema = UserRequestSchema.parser
auth_request_schema = AuthRequestSchema.parser

@api.route("/")
class UserRoutes(Resource):
    """
        User routes
        api/v1/users/
    """
    @admin_required
    def post(self):
        """
            handle post request
            Add User
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            user = UserSchema(strict=True).load(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try
        response = UserServices.add(user.data, request_data["password"])
        return response

    @admin_required
    def get(self):
        """
            handle get request
            Return all user registered under api key
        """
        # fetch api object from header
        response = UserServices.show_all()
        return response
    #end def

@api.route("/<string:user_id>")
class UserInfoRoutes(Resource):
    """
        users routes
        api/v1/users/<user_id>
    """
    @admin_required
    def get(self, user_id):
        """
            Handle GET Request
            return single user information
        """
        # fetch api object from header
        response = UserServices(user_id).info()
        return response
    #end def

    @admin_required
    def put(self, user_id):
        """
            handle put request
            Update User information
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            user = UserSchema().validate(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try
        response = UserServices(user_id).update(request_data)
        return response

    @admin_required
    def delete(self, user_id):
        """
            Handle DELETE Request
            remove user
        """
        # fetch api object from header
        response = UserServices(user_id).remove()
        return response
    #end def

@api.route("/<string:user_id>/enroll/<string:candidate_id>")
class UserEnrollmentRoutes(Resource):
    """
        User Enrollment
    """
    @admin_required
    def post(self, user_id, candidate_id):
        """
            Enroll user as candidate
        """
        response = UserServices(user_id, candidate_id).enroll()
        return response
        
    @admin_required
    def delete(self, user_id, candidate_id):
        """
            Unroll User As Candidate
        """
        # fetch api object from header
        response = UserServices(user_id, candidate_id).unroll()
        return response
    #end def
