"""
    Test Models
"""
from app.test.base  import BaseTestCase

from app.api import db

from app.api.models import *

class UserTest(BaseTestCase):
    """ test user model """

    def test_create(self):
        """ test adding user to database """
        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        user = User.query.get(user.id)


    def test_check_password(self):
        """ test method that checking user password"""
        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        result = user.check_password("password")
        self.assertTrue(result)

class ElectionTest(BaseTestCase):

    def test_create_election(self):
        election = Election(
            name="ELECTION_1",
            images="SOME_IMAGE_PATH",
            description="description"
        )
        db.session.add(election)
        db.session.commit()

class CandidateTest(BaseTestCase):

    def test_create_candidate(self):
        election = Election(
            name="ELECTION_1",
            images="SOME_IMAGE_PATH",
            description="description"
        )
        db.session.add(election)
        db.session.commit()

        # ADD DUMY USER
        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        user2 = User(username="krystal",
                    identity_id="113456",
                    name="Krystal",
                    msisdn="081214341234",
                    email="krystal@bp.com",
                   )
        user2.set_password("password")

        db.session.add(user2)
        db.session.commit()

        candidate = Candidate(
            name="CANDIDATE_1",
            description="description",
            election_id=election.id
        )
        db.session.add(candidate)
        db.session.commit()

        candidate2 = Candidate(
            name="CANDIDATE_2",
            description="description",
            election_id=election.id
        )
        db.session.add(candidate2)
        db.session.commit()

        # ENROLL USER AS CANDIDATE
        user.candidate_id = candidate.id
        user2.candidate_id = candidate.id
        db.session.commit()

        print(election.candidates)
        print(election.candidates[0].users)

class VoteTest(BaseTestCase):

    def test_vote_election(self):
        election = Election(
            name="ELECTION_1",
            images="SOME_IMAGE_PATH",
            description="description"
        )
        db.session.add(election)
        db.session.commit()

        # ADD DUMMY USER 
        user = User(username="jennie",
                    identity_id="123456",
                    name="Kim Jennie",
                    msisdn="081212341234",
                    email="jennie@bp.com",
                   )
        user.set_password("password")

        db.session.add(user)
        db.session.commit()

        user2 = User(username="krystal",
                    identity_id="113456",
                    name="Krystal",
                    msisdn="081214341234",
                    email="krystal@bp.com",
                   )
        user2.set_password("password")

        db.session.add(user2)
        db.session.commit()

        candidate = Candidate(
            name="CANDIDATE_1",
            description="description",
            election_id=election.id
        )
        db.session.add(candidate)
        db.session.commit()

        candidate2 = Candidate(
            name="CANDIDATE_2",
            description="description",
            election_id=election.id
        )
        db.session.add(candidate2)
        db.session.commit()

        # ENROLL USER AS CANDIDATE
        user.candidate_id = candidate.id
        user2.candidate_id = candidate.id
        db.session.commit()

        vote = Vote(
            candidate_id=candidate.id,
            user_id=user.id
        )
        db.session.add(vote)
        db.session.commit()

        vote = Vote(
            candidate_id=candidate.id,
            user_id=user2.id
        )
        db.session.add(vote)
        db.session.commit()

        print(election.candidates[0].votes)
