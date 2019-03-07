"""
    Election Routes
"""
from werkzeug.utils import secure_filename
from flask_restplus import Resource

from marshmallow import ValidationError

from app.api.election import api

# flask rest plus extesnion
from app.api.request_schema import *
from app.api.serializer import *
# services
from app.api.election.modules.election_services import ElectionServices
from app.api.election.modules.candidate_services import CandidateServices
# exception
from app.api.error.http import *

from app.api.utility.utils import upload
from app.config import config

ERROR = config.Config.ERROR
request_schema = ElectionRequestSchema.parser

@api.route("/")
class ElectionRoutes(Resource):
    """
        Election routes
        api/v1/elections/
    """
    def post(self):
        """
            handle post request
            Add Election
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            election = ElectionSchema(strict=True).load(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)

        # upload file here
        filename = upload(request_data["images"])

        response = ElectionServices.add(election.data, filename)
        return response

    def get(self):
        """
            handle get request
            Return all user registered under api key
        """
        # fetch api object from header
        response = ElectionServices.show_all()
        return response
    #end def

@api.route("/<string:election_id>")
class ElectionInfoRoutes(Resource):
    """
        Election routes
        api/v1/elections/<election_id>
    """
    def get(self, election_id):
        """
            Handle GET Request
            return single election information
        """
        # fetch api object from header
        response = ElectionServices(election_id).info()
        return response
    #end def

    def put(self, election_id):
        """
            handle put request
            Update User information
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            user = ElectionSchema(strict=True).validate(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try

        # upload file here
        filename = upload(request_data["images"])
        request_data["images"] = filename

        response = ElectionServices(election_id).update(request_data)
        return response

    def delete(self, election_id):
        """
            Handle DELETE Request
            remove user
        """
        # fetch api object from header
        response = ElectionServices(election_id).remove()
        return response
    #end def

@api.route("/<string:election_id>/candidates/")
class CandidateRoutes(Resource):
    """
        Election routes
        api/v1/elections/election_id/candidates
    """
    def post(self, election_id):
        """
            handle post request
            Add Election
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            candidate = CandidateSchema(strict=True).load(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try

        # upload file here
        filename = upload(request_data["images"])

        response = CandidateServices(election_id).add(candidate.data, filename)
        return response

    def get(self, election_id):
        """
            handle get request
            Return all user registered under api key
        """
        # fetch api object from header
        response = CandidateServices(election_id).show_all()
        return response
    #end def

@api.route("/<string:election_id>/candidates/<string:candidate_id>")
class CandidateInfoRoutes(Resource):
    """
        Election routes
        api/v1/elections/election_id/candidates/candidate_id
    """
    def get(self, election_id, candidate_id):
        """
            handle get request
            Return all user registered under api key
        """
        # fetch api object from header
        response = CandidateServices(election_id, candidate_id).info()
        return response
    #end def

    def put(self, election_id, candidate_id):
        """
            handle post request
            Add Election
        """
        request_data = request_schema.parse_args(strict=True)
        try:
            candidate = CandidateSchema(strict=True).load(request_data)
        except ValidationError as error:
            raise BadRequest(ERROR["INVALID_PARAMETER"]["TITLE"],
                             ERROR["INVALID_PARAMETER"]["MESSAGE"],
                             error.messages)
        #end try

        # upload file here
        request_data["images"] = upload(request_data["images"])
        response = CandidateServices(election_id, candidate_id).update(request_data)
        return response

    def delete(self, election_id, candidate_id):
        """
            handle get request
            Return all user registered under api key
        """
        # fetch api object from header
        response = CandidateServices(election_id, candidate_id).remove()
        return response
    #end def
