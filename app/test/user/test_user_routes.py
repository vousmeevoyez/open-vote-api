"""
    User Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

class TestUserRoutes(BaseTestCase):
    """ Test User Routes Class"""

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
        self.assertEqual(result.status_code, 200)
        body = result.get_json()
        self.assertEqual(body["data"]["email"], "jennie@bp.com")

    def test_create_user_remove(self):
        """ test successfully create user and remove user"""
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

        result = self.remove_user(user_id)
        self.assertEqual(result.status_code, 204)

    def test_create_user_update(self):
        """ test successfully create user and update user"""
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

        result = self.update_user({
            "name"       : "Rose blackpink",
            "identity_id": "12345678911",
            "msisdn"     : "081212341232",
            "email"      : "rose@bp.com",
            "role"       : "PARTICIPANT",
            "password"   : "password",
        }, user_id)
        self.assertEqual(result.status_code, 204)

    def test_enroll_user(self):
        """ test api call to create candidates for specific election and enroll
        the user """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)

        response = result.get_json()
        candidate_id = response["data"]["candidate_id"]

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

        result = self.enroll_user(user_id, candidate_id)
        self.assertEqual(result.status_code, 204)

    def test_unroll_user(self):
        """ test api call to create candidates for specific election and enroll
        the user """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)

        response = result.get_json()
        candidate_id = response["data"]["candidate_id"]

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

        result = self.enroll_user(user_id, candidate_id)
        self.assertEqual(result.status_code, 204)

        result = self.unroll_user(user_id, candidate_id)
        self.assertEqual(result.status_code, 204)
