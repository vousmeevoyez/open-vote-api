"""
    Test Decorator
"""
#pylint: disable=import-error
#pylint: disable=unused-import
from unittest import mock
from unittest.mock import patch, Mock

from app.api import db

from app.test.base import BaseTestCase
from app.api.models import *

# import all decorator
from app.api.auth.decorators import *
from app.api.auth.decorators import _parse_token
from app.api.auth.modules.auth_services import AuthServices

from app.api.error.token import *

from app.api.error.http import *
# import all routes

class TestAuthDecorator(BaseTestCase):
    """ test auth decorator"""

    def setUp(self):
        super().setUp()
        """ test encode a token"""
        # create dummy user
        user = User(
            username='lisabp',
            name='lisa',
            email='lisa@bp.com',
            msisdn='081219644314',
            role=3,
        )
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        result = AuthServices("lisabp").login("password")

        self.token = result[0]["data"]["access_token"]
    #end def

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_parse_token(self, parse_args_mock):
        """ test parse token and return token """
        parse_args_mock.return_value = {
            "Authorization" : "Bearer some_token"
        }

        result = _parse_token()
        self.assertEqual(result, "some_token")

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_parse_token_empty(self, parse_args_mock):
        """ test parse token and return token """
        parse_args_mock.return_value = {
            "Authorization" : ""
        }

        with self.assertRaises(ParseError):
            result = _parse_token()

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_parse_token_failed(self, parse_args_mock):
        """ test parse token and return token """
        parse_args_mock.return_value = {
            "Authorization" : "jlkajsdljalsjldjas"
        }

        with self.assertRaises(ParseError):
            result = _parse_token()

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_admin_required_failed(self, parse_args_mock):
        """ test admin required decorator with invalid token"""
        func = Mock()

        decorated_func = admin_required(func)

        parse_args_mock.return_value = {
            "Authorization" : "jlkajsdljalsjldjas"
        }

        with self.assertRaises(BadRequest):
            result = decorated_func()

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_admin_required_invalid_identifier(self, parse_args_mock):
        """ test admin required decorator with valid token but invalid user """
        func = Mock()

        decorated_func = admin_required(func)

        parse_args_mock.return_value = {
            "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwidHlwZSI6IkFDQ0VTUyJ9.7qJycMO9pCUr9VwQZolkko_Ft0EcOVbwWFlkBOfuKVE"
        }

        with self.assertRaises(BadRequest):
            result = decorated_func()

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_token_required(self, parse_args_mock):
        """ test get token """
        func = Mock()

        decorated_func = token_required(func)

        parse_args_mock.return_value = {
            "Authorization" : "Bearer {}".format(self.token)
        }

        result = decorated_func()

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_get_token_payload(self, parse_args_mock):
        """ test get token """
        parse_args_mock.return_value = {
            "Authorization" : "Bearer {}".format(self.token)
        }

        result = get_token_payload()
        self.assertTrue(result["token_type"])
        self.assertTrue(result["user_id"])

    @mock.patch("flask_restplus.reqparse.RequestParser.parse_args")
    def test_get_current_token(self, parse_args_mock):
        """ test get token """
        parse_args_mock.return_value = {
            "Authorization" : "Bearer {}".format(self.token)
        }

        result = get_current_token()
        self.assertEqual(result, self.token)
