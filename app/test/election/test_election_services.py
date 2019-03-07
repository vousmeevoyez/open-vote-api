"""
    Test User Services
"""
from app.test.base  import BaseTestCase

from app.api.election.modules.election_services import ElectionServices

from app.api import db

from app.api.models import *

from app.api.error.http import *

class TestElectionServices(BaseTestCase):
    """ testing class for all method for election services"""
    def _create_election(self):
        election = Election(
            name="ELECTION",
            images="IMAGE_PATH",
            description="Some Description",
        )
        db.session.add(election)
        db.session.commit()
        return election

    def test_add(self):
        """ test function that adding api key"""
        election = self._create_election()
        result = ElectionServices.add(election, "some_filename")

        self.assertEqual(result[1], 201)

    def test_show_all(self):
        """ test function that show all election """
        election = self._create_election()
        result = ElectionServices.add(election, "some_filename")
        self.assertEqual(result[1], 201)

        result = ElectionServices.show_all()
        self.assertTrue(result[0]["data"])

    def test_info(self):
        """ test function that show all election """
        election = self._create_election()
        result = ElectionServices.add(election, "some_filename")
        self.assertEqual(result[1], 201)
        key = result[0]["data"]["election_id"]

        result = ElectionServices(key).info()
        self.assertTrue(result[0]["data"])

    def test_remove(self):
        """ test function that remove election"""
        election = self._create_election()
        result = ElectionServices.add(election, "some_filename")
        self.assertEqual(result[1], 201)
        key = result[0]["data"]["election_id"]

        result = ElectionServices(key).remove()
        self.assertEqual(result[1], 204)
