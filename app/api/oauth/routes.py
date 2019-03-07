"""
    User Routes
"""
from flask_restplus import Resource
from werkzeug.security import gen_salt

from marshmallow import ValidationError

from app.api.oauth import api

# flask rest plus extesnion
from app.api.request_schema import *
#from app.api.serializer import UserSchema
# services
from app.api.models import *

from app.api.utility.utils import string_to_uuid

request_schema = ClientRequestSchema.parser

@api.route("/client/<string:user_id>")
class ClientRoutes(Resource):
    """
        Register Client Here
        api/v1/oauth/client
    """
    def post(self, user_id):
        """
            handle post request
            return token
        """
        request_data = request_schema.parse_args(strict=True)
        '''
        try:
            excluded = ("id", "name", "identity_id", "msisdn", "email",
                        "password", "role")
            user = UserSchema(strict=True).validate(request_data, partial=excluded)
        except ValidationError as error:
            raise SerializeError(error.messages)
        #end try
        '''
        user = User.query.filter_by(id=string_to_uuid(user_id)).first()
        client = Client(**request_data)
        client.user_id = user.id
        client.client_id = gen_salt(24)
        if client.token_endpoint_auth_method == 'none':
            client.client_secret = ''
        else:
            client.client_secret = gen_salt(48)

        return { "message" : "client successfully created"}
    #end def

@api.route("/authorize/<string:user_id>")
class AuthorizeRoutes(Resource):
    def post(self):
