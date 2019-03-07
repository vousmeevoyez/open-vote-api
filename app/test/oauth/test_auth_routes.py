"""
    User Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

BASE_URL = "/api/v1"
RESOURCE = "/oauth/"

class TestOauthRoutes(BaseTestCase):
    """ Test Oauth Routes Class"""
    def create_user(self, params):
        """ function to create user by accessing user url API"""
        return self.client.post(
            BASE_URL + "/users/",
            data=dict(
                username=params["username"],
                name=params["name"],
                identity_id=params["identity_id"],
                msisdn=params["msisdn"],
                email=params["email"],
                password=params["password"],
                role=params["role"]
            ),
        )
    #end def

    def create_client(self, params, user_id):
        """ function to create user by accessing user url API"""
        return self.client.post(
            BASE_URL + RESOURCE + "client/" + user_id,
            data=dict(
                client_name=params["client_name"],
                client_uri=params["client_uri"],
                scope=params["scope"],
                redirect_uri=params["redirect_uri"],
                grant_type=params["grant_type"],
                response_type=params["response_type"],
                token_endpoint_auth_method=params["token_endpoint_auth_method"]
            ),
        )
    #end def

    def test_create_client(self):
        """ test successfully create user """
        result = self.create_user({
            "username"   : "jennie",
            "name"       : "Kim Jennie",
            "identity_id": "12345678910",
            "msisdn"     : "081212341234",
            "email"      : "jennie@bp.com",
            "role"       : "ADMIN",
            "password"   : "password",
        })
        response = result.get_json()
        user_id = response["data"]["user_id"]
        self.assertEqual(result.status_code, 201)

        result = self.create_client({
            "client_name"   : "some client name",
            "client_uri"    : "client uri",
            "scope"         : "some scope",
            "redirect_uri"  : "redirect uri",
            "grant_type"    : "grant type",
            "response_type" : "response type",
            "token_endpoint_auth_method" : "none",
        }, user_id)
        print(result.get_json())
        self.assertEqual(result.status_code, 201)
