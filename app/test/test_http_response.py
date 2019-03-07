"""
    Test HTTP Response
"""
from app.test.base  import BaseTestCase

from app.api.http_response import *

class TestHTTPResponse(BaseTestCase):
    """ HTTP Response test class"""

    def test_no_content(self):
        """ test no content HTTP response """
        result = no_content()
        self.assertEqual(result[1], 204)

    def test_created(self):
        """ test created HTTP response """
        result = created()
        self.assertEqual(result[1], 201)

    def test_created_message_data(self):
        """ test created HTTP response and set data and set message"""
        result = created("some data", "some message")
        self.assertEqual(result[1], 201)
        self.assertTrue(result[0]["data"])
        self.assertTrue(result[0]["message"])

    def test_accepted(self):
        """ test accepted HTTP response """
        result = accepted("message")
        self.assertEqual(result[1], 202)
        self.assertTrue(result[0]["message"])
