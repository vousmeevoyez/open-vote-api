"""
    Test User Services
"""
from app.test.base  import BaseTestCase

from app.api.election.modules.election_services import ElectionServices
from app.api.election.modules.candidate_services import CandidateServices

from app.api import db

from app.api.models import *

from app.api.error.http import *

class TestCandidateServices(BaseTestCase):
    """ testing class for all method for election services"""
    def _create_election(self):
        election = Election(
            name="ELECTION",
            images="IMAGE_PATH",
            description="Some Description",
        )
        db.session.add(election)
        db.session.commit()

        result = ElectionServices.add(election, "somefilename")
        return result[0]["data"]["election_id"]

    def test_add_candidate(self):
        election_id = self._create_election()

        candidate = Candidate(
            name="CAndidate1",
            images="some_images",
            description="Some candidate description",
        )
        response = CandidateServices(api_key, election_id).add(candidate, "somefilename")
        self.assertEqual(response[1], 201)

    def test_info_candidate(self):
        election_id = self._create_election()

        candidate = Candidate(
            name="CAndidate1",
            images="some_images",
            description="Some candidate description",
        )
        response = CandidateServices(api_key, election_id).add(candidate, "somefilename")
        self.assertEqual(response[1], 201)
        candidate_id = response[0]["data"]["candidate_id"]

        response = CandidateServices(api_key, election_id, candidate_id).info()
        print(response)
