"""
    Test Vote Services
"""
from app.test.base  import BaseTestCase

from app.api.vote.modules.vote_services import VoteServices

from app.api import db

from app.api.models import Vote, Candidate, Election, User

from app.api.error.http import *

class TestVoteServices(BaseTestCase):
    """ testing class for all method for vote services"""

    def setUp(self):
        super().setUp()

        # create dummy candidate first
        election = Election(
            name="ELECTION",
            images="IMAGE_PATH",
            description="Some Description",
        )
        db.session.add(election)
        db.session.commit()

        candidate = Candidate(
            name="CAndidate1",
            images="some_images",
            description="Some candidate description",
            election_id=election.id
        )
        db.session.add(candidate)
        db.session.commit()

        user = User(username="jennie",
                    name="Kim Jennie",
                    email="jennie@bp.com",
                    identity_id="123456789",
                    msisdn="081212341234",
                    role=1)
        db.session.add(user)
        db.session.commit()

        self.candidate_id = str(candidate.id)
        self.user_id = str(user.id)

    def test_cast(self):
        """ test function that cast a vote"""
        result = VoteServices(self.user_id).cast(self.candidate_id)
        self.assertEqual(result[1], 201)

    def test_cast_again(self):
        """ test function that cast a vote with same user """
        result = VoteServices(self.user_id).cast(self.candidate_id)
        self.assertEqual(result[1], 201)

        with self.assertRaises(UnprocessableEntity):
            result = VoteServices(self.user_id).cast(self.candidate_id)

    def test_count_vote(self):
        """ test function that count a vote"""
        result = VoteServices(self.user_id).cast(self.candidate_id)
        self.assertEqual(result[1], 201)

        result = VoteServices.count(self.candidate_id)
        self.assertEqual(result[1], 200)
