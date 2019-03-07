"""
    User Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

BASE_URL = "/api/v1"
RESOURCE = "/users/"

class TestUserRoutes(BaseTestCase):
    """ Test User Routes Class"""

    def create_api_key(self, name, email):
        """ function to create api key by accessing token url API"""
        return self.client.post(
            BASE_URL + "/keys/",
            data=dict(
                name=name,
                email=email
            )
        )
    #end def

    def create_user(self, params, api_key):
        """ function to create user by accessing user url API"""
        headers = {
            'X-Api-Key': '{}'.format(api_key)
        }
        return self.client.post(
            BASE_URL + RESOURCE,
            data=dict(
                username=params["username"],
                name=params["name"],
                identity_id=params["identity_id"],
                msisdn=params["msisdn"],
                email=params["email"],
                password=params["password"],
                role=params["role"]
            ),
            headers=headers
        )
    #end def

    def user_info(self, user_id, api_key):
        """ function to return api key info """
        headers = {
            'X-Api-Key': '{}'.format(api_key)
        }
        return self.client.get(
            BASE_URL + RESOURCE + user_id,
            headers=headers
        )
    #end def

    def test_create_user(self):
        """ test successfully create user """
        result = self.create_api_key("jennie", "jennie@blackpink.com")
        response = result.get_json()
        api_key = response["data"]["api_key"]

        result = self.create_user({
            "username"   : "jennie",
            "name"       : "Kim Jennie",
            "identity_id": "12345678910",
            "msisdn"     : "081212341234",
            "email"      : "jennie@bp.com",
            "role"       : "ADMIN",
            "password"   : "password",
        }, api_key)
        self.assertEqual(result.status_code, 201)

    def test_create_user_info(self):
        """ test successfully create user and get user info"""
        result = self.create_api_key("jennie", "jennie@blackpink.com")
        response = result.get_json()
        api_key = response["data"]["api_key"]

        result = self.create_user({
            "username"   : "jennie",
            "name"       : "Kim Jennie",
            "identity_id": "12345678910",
            "msisdn"     : "081212341234",
            "email"      : "jennie@bp.com",
            "role"       : "ADMIN",
            "password"   : "password",
        }, api_key)
        response = result.get_json()
        user_id = response["data"]["user_id"]
        self.assertEqual(result.status_code, 201)

        result = self.user_info(user_id, api_key)
        print(result.get_json())
