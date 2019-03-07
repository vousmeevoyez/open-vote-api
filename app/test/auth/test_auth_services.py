"""
    Test User Services
"""
from unittest import mock
from unittest.mock import patch, Mock

from app.test.base  import BaseTestCase

from app.api.auth.modules.auth_services import AuthServices

from app.api import db

from app.api.models import User

from app.api.utility.utils import string_to_uuid

from app.api.error.http import *
from app.api.error.token import *

class TestAuthServices(BaseTestCase):
    """ testing class for all method for user services"""

    def setUp(self):
        super().setUp()

        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

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

    def test_current_login_user(self):
        """ test curren login user"""
        result = AuthServices("EVOTESUPERADMIN").login("password")
        token = result[0]["data"]["access_token"]

        result = AuthServices._current_login_user(token)

        self.assertEqual(result["token_type"], "ACCESS")

    def test_current_login_user_invalid(self):
        """ test curren login user"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwidHlwZSI6IkFDQ0VTUyJ9.9JeY4v711wDsUzczKNlR84IMTTab5KwraY4rlQ3jaAQ"
        with self.assertRaises(BadRequest):
            result = AuthServices._current_login_user(token)

    @patch.object(User, "decode_token")
    def test_current_login_user_revoked_token(self, mock_decode):
        """ test curren login user but using revoked token"""

        mock_decode.side_effect = RevokedTokenError
        with self.assertRaises(Unauthorized):
            AuthServices._current_login_user("lkadsjlkjaskljdkjaskdjlajldaslkjdak")

    @patch.object(User, "decode_token")
    def test_current_login_user_signature_expired_token(self, mock_decode):
        """ test curren login user but using signature expired token """

        mock_decode.side_effect = SignatureExpiredError(Mock())
        with self.assertRaises(Unauthorized):
            AuthServices._current_login_user("lkadsjlkjaskljdkjaskdjlajldaslkjdak")

    @patch.object(User, "decode_token")
    def test_current_login_user_invalid_token(self, mock_decode):
        """ test curren login user but using invalid token """

        mock_decode.side_effect = InvalidTokenError(Mock())
        with self.assertRaises(BadRequest):
            AuthServices._current_login_user("lkadsjlkjaskljdkjaskdjlajldaslkjdak")

    @patch.object(User, "decode_token")
    def test_current_login_user_empty_payload(self, mock_decode):
        """ test curren login user but using empty payload token"""

        mock_decode.side_effect = EmptyPayloadError
        with self.assertRaises(Unauthorized):
            AuthServices._current_login_user("lkadsjlkjaskljdkjaskdjlajldaslkjdak")
