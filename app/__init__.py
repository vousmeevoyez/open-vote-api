from flask_restplus import Api

from flask import Blueprint

from app.api.oauth import api as auth_ns
from app.api.user import api as user_ns
from app.api.election import api as election_ns
from app.api.static import api as static_ns


blueprint = Blueprint("api", __name__)

class CustomApi(Api):
    """ Custom API Classs """
    def handle_error(self, e):
        """ Overrides the handle_error() method of the Api and adds custom error handling
        :param e: error object
        """
        code = getattr(e, 'code', 500)  # Gets code or defaults to 500
        message = getattr(e, 'message', 'INTERNAL_SERVER_ERROR')
        to_dict = getattr(e, 'to_dict', None)

        if code == 500:
            # capture error and send to sentry
            sentry.captureException(e)
            data = {'error': message}

        # handle request schema error from reqparse
        if code == 400:
            response = getattr(e, 'response', True)
            if response is None:
                # build error response
                data = {
                    "error" : "MISSING_PARAMETER",
                    "message" : e.data['message'],
                    "details" : e.data['errors']
                }

        if to_dict:
            data = to_dict()    

        return self.make_response(data, code)

api = CustomApi(blueprint,
                contact="kelvindsmn@gmail.com")

api.add_namespace(user_ns, path="/users")
api.add_namespace(auth_ns, path="/oauth")
api.add_namespace(election_ns, path="/elections")
api.add_namespace(static_ns, path="/static")
