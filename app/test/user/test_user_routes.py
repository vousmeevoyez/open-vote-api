"""
    User Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

BASE_URL = "/api/v1"
RESOURCE = "/users/"

class TestUserRoutes(BaseTestCase):
    """ Test User Routes Class"""
    def create_user(self, params):
        """ function to create user by accessing user url API"""
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
            )
        )
    #end def

    def user_info(self, user_id):
        """ function to return api key info """
        return self.client.get(
            BASE_URL + RESOURCE + user_id,
        )
    #end def

    def test_create_user(self):
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
        self.assertEqual(result.status_code, 201)

    def test_create_user_info(self):
        """ test successfully create user and get user info"""
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

        result = self.user_info(user_id)
        print(result.get_json())
