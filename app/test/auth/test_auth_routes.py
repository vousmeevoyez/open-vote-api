"""
    User Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

class TestAuthRoutes(BaseTestCase):
    """
        This where we test all API Call
    """
    def test_login(self):
        """
            Test CASE 1 : Try login using superadmin credentials
        """
        response = self.get_token({
            "username" : "EVOTESUPERADMIN",
            "password" : "password"
        })

        # make sure return 200
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        # make sure return access token
        self.assertTrue(body["data"]["access_token"])

    def test_login_failed(self):
        """
            Test CASE 2 : Try login using invalid username
        """
        response = self.get_token({
            "username" : "someinvalidusername",
            "password" : "password"
        })

        # make sure return 404
        self.assertEqual(response.status_code, 404)
        body = response.get_json()
        # make sure return correct error titles
        self.assertEqual(body["error"], "USER_NOT_FOUND")

        """
            Test CASE 3 : Try login using invalid password
        """
        response = self.get_token({
            "username" : "EVOTESUPERADMIN",
            "password" : "p0ssword"
        })

        # make sure return 401
        self.assertEqual(response.status_code, 401)
        body = response.get_json()
        # make sure return correct error titles
        self.assertEqual(body["error"], "INVALID_LOGIN")

    def test_logout(self):
        """
            Test CASE 1 : Try logout using valid token
        """
        response = self.get_token({
            "username" : "EVOTESUPERADMIN",
            "password" : "password"
        })

        # make sure return 200
        self.assertEqual(response.status_code, 200)
        body = response.get_json()

        token = body["data"]["access_token"]

        response = self.revoke_token(token)
        # make sure return 204
        self.assertEqual(response.status_code, 204)

    def test_logout_failed(self):
        """
            Test CASE 2 : Try logout using token that already blacklisted
        """
        response = self.get_token({
            "username" : "EVOTESUPERADMIN",
            "password" : "password"
        })

        # make sure return 200
        self.assertEqual(response.status_code, 200)
        body = response.get_json()

        token = body["data"]["access_token"]

        response = self.revoke_token(token)
        self.assertEqual(response.status_code, 204)

        response = self.revoke_token(token)
        # should return 401
        self.assertEqual(response.status_code, 401)
        body = response.get_json()
        self.assertEqual(body["error"], "REVOKED_TOKEN")
