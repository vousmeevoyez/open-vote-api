"""
    Votes Routes
"""
from werkzeug.utils import secure_filename
from flask_restplus import Resource
from marshmallow import ValidationError

# blueprint
from app.api.vote import api
# flask rest plus extesnion
from app.api.request_schema import *
from app.api.serializer import *
# services
from app.api.vote.modules.vote_services import VoteServices
# exception
from app.api.error.http import *
# decorators
from app.api.auth.decorators import get_token_payload, token_required, admin_required
from app.config import config

ERROR = config.Config.ERROR

@api.route("/<string:candidate_id>")
class VoteRoutes(Resource):
    """
        Vote routes
        api/v1/votes/candidate_id
    """
    @token_required
    def post(self, candidate_id):
        """
            cast a vote
        """
        payload = get_token_payload()
        user_id = payload["user_id"]

        response = VoteServices(user_id).cast(candidate_id)
        return response

    @admin_required
    def get(self, candidate_id):
        """
            count a vote
        """
        # fetch api object from header
        response = VoteServices.count(candidate_id)
        return response
    #end def
