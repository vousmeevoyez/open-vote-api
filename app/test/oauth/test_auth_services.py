"""
    Test User Services
"""
from app.test.base  import BaseTestCase

from app.api.user.modules.user_services import UserServices
from app.api.auth.modules.auth_services import AuthServices

from app.api import db

from app.api.models import User
from app.api.models import ApiKey

from app.api.utility.utils import string_to_uuid

from app.api.error.http import *

class TestAuthServices(BaseTestCase):
    """ testing class for all method for user services"""

    def setUp(self):
        super().setUp()

        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                    api_id=api_key.id,
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        self.user = user

    def test_generate_token(self):
        """ test function that generate user JWT Token"""
        result = AuthServices("jennie").generate_token()
        self.assertTrue(isinstance(result, str))

    def test_revoke_token(self):
        """ test function that generate user JWT Token"""
        result = AuthServices("jennie").generate_token()
        self.assertTrue(isinstance(result, str))

        result = AuthServices.revoke(result)
        self.assertEqual(result[1], 204)

    def test_decode_token(self):
        token = AuthServices("jennie").generate_token()
        result = AuthServices.decode_token(token)
        self.assertEqual(result, self.user)

    def test_decode_token_already_blacklisted(self):
        token = AuthServices("jennie").generate_token()
        result = AuthServices.revoke(token)
        self.assertEqual(result[1], 204)

        with self.assertRaises(Unauthorized):
            result = AuthServices.decode_token(token)

    def test_decode_token_already_blacklisted(self):
        token = AuthServices("jennie").generate_token()
        result = AuthServices.revoke(token)
        self.assertEqual(result[1], 204)

        with self.assertRaises(Unauthorized):
            result = AuthServices.decode_token(token)

    def test_login(self):
        """ test function that checking user login"""
        result = AuthServices("jennie").login("password")
        self.assertTrue(result[0]["data"])

    def test_login_not_found(self):
        """ test function that checking user login but not found the username"""
        with self.assertRaises(RequestNotFound):
            result = AuthServices("janejane").login("password")

    def test_login_incorrect_password(self):
        """ test function that checking user login but invalid password"""
        with self.assertRaises(Unauthorized):
            result = AuthServices("jennie").login("passw0rd")
