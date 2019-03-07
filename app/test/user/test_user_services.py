"""
    Test User Services
"""
from app.test.base  import BaseTestCase

from app.api.user.modules.user_services import UserServices

from app.api import db

from app.api.models import User

from app.api.error.http import *

class TestUserServices(BaseTestCase):
    """ testing class for all method for user services"""

    def _create_user(self):
        user = User(username="jennie",
                    name="Kim Jennie",
                    email="jennie@bp.com",
                    identity_id="123456789",
                    msisdn="081212341234",
                    role=1)
        result = UserServices.add(user, "password")

        user_id = result[0]["data"]["user_id"]

        # return object and id so it can be reused across unit tests
        response = {
            "object" : user,
            "id" : user_id,
        }
        return response

    def test_add(self):
        """ test function that adding api key"""
        response = self._create_user()
        self.assertTrue(response["object"])
        self.assertTrue(response["id"])

    def test_info(self):
        """ test function that adding api key"""
        response = self._create_user()

        user_id = response["id"]

        result = UserServices(user_id).info()

        response = result["data"]
        self.assertTrue(response["identity_id"])
        self.assertTrue(response["msisdn"])
        self.assertTrue(response["email"])
        self.assertTrue(response["role"])
        self.assertTrue(response["username"])
        self.assertTrue(response["created_at"])
        self.assertTrue(response["status"])
        self.assertTrue(response["name"])

    def test_remove(self):
        """ test function that remove user """
        response = self._create_user()

        user_id = response["id"]

        result = UserServices(user_id).remove()
        self.assertEqual(result[1], 204)


        with self.assertRaises(RequestNotFound):
            result = UserServices(user_id).info()


    def test_update(self):
        """ test function that update user """
        response = self._create_user()
        user_id = response["id"]

        data = {
            "identity_id" : "1111111",
            "name"        : "Kim Jisoo",
            "email"       : "jisoo@gmail.com",
            "role"        : "ADMIN",
            "status"      : True,
            "msisdn"      : "08661111222",
            "password"    : "oasswird",
        }

        result = UserServices(user_id).update(data)
        self.assertEqual(result[1], 204)

        # check data and make sure its updated
        result = UserServices(user_id).info()

        response = result["data"]
        self.assertEqual(response["identity_id"], data["identity_id"])
        self.assertEqual(response["name"], data["name"])
        self.assertEqual(response["email"], data["email"])

    def test_show_all(self):
        """ test function that return user registered on certain api id"""
        # create user and register the api id
        response = self._create_user()

        result = UserServices.show_all()
        self.assertEqual(len(result[0]["data"]), 1)
