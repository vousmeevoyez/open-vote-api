"""
    Test Utility
"""
import uuid
from app.test.base  import BaseTestCase

from app.api.utility.utils import uuid_to_string
from app.api.utility.utils import string_to_uuid
from app.api.utility.utils import DecodeError
from app.api.utility.utils import generate_file_name

class TestUtility(BaseTestCase):
    """ test utility class """

    def test_uuid_to_string(self):
        """ test uuid to string """
        uuid_key = uuid.uuid4().bytes
        result = uuid_to_string(uuid_key)
        self.assertTrue(isinstance(result, str))

    def test_string_to_uuid(self):
        """ string to uuid """
        uuid_key = uuid.uuid4().bytes
        result = uuid_to_string(uuid_key)
        self.assertTrue(isinstance(result, str))

        result = string_to_uuid(result)
        self.assertTrue(isinstance(result, str))

    def test_generate_filename(self):
        """ test generate file name"""
        result = generate_file_name("Screen Shot 2018-12-27 at 06.24.00.png")
        print(result)
        self.assertTrue(isinstance(result, str))
