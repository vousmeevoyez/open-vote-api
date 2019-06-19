"""
    Base Test
"""
from flask_testing  import TestCase

from manage  import app, init
from app.api import db
# configuration
from app.config import config
# models

TEST_CONFIG = config.TestingConfig

BASE_URL = "/v1"

class BaseTestCase(TestCase):
    """ This is Base Tests """

    def create_app(self):
        app.config.from_object(TEST_CONFIG)
        return app

    def setUp(self):
        db.create_all()
        self.initialize_test()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def initialize_test(self):
        init() # call init fucntion from manage py 
        result = self.get_token({
            "username" : "EVOTESUPERADMIN",
            "password" : "password"
        })
        response = result.get_json()
        token = response["data"]["access_token"]
        self._token = token

    """
        API CALL
    """
    """
        USER
    """
    def create_user(self, params):
        """ api call to create user"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.post(
            BASE_URL + "/users/",
            data=dict(
                username=params["username"],
                name=params["name"],
                identity_id=params["identity_id"],
                msisdn=params["msisdn"],
                email=params["email"],
                password=params["password"],
                role=params["role"]
            ),
            headers=headers
        )
    #end def

    def update_user(self, params, user_id):
        """ api call to update user"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.put(
            BASE_URL + "/users/"+ user_id,
            data=dict(
                name=params["name"],
                identity_id=params["identity_id"],
                msisdn=params["msisdn"],
                email=params["email"],
                password=params["password"],
                role=params["role"]
            ),
            headers=headers
        )
    #end def

    def user_info(self, user_id):
        """ api call to get user info"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.get(
            BASE_URL + "/users/" + user_id,
            headers=headers
        )
    #end def

    def remove_user(self, user_id):
        """ api call to remove user"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.delete(
            BASE_URL + "/users/" + user_id,
            headers=headers
        )
    #end def

    def enroll_user(self, user_id, candidate_id):
        """ api call to enroll as candiate"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.post(
            BASE_URL + "/users/" + user_id + "/enroll/" + candidate_id,
            headers=headers
        )
    #end def

    def unroll_user(self, user_id, candidate_id):
        """ api call to unroll as candiate"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.delete(
            BASE_URL + "/users/" + user_id + "/enroll/" + candidate_id,
            headers=headers
        )
    #end def

    """
        Authentication
    """
    def get_token(self, params):
        """ function to get access token"""
        return self.client.post(
            BASE_URL + "/auth/login",
            data=dict(
                username=params["username"],
                password=params["password"],
            )
        )
    #end def

    def revoke_token(self, token):
        """ function to get revoke token"""
        headers = {
            "Authorization" : "Bearer {}".format(token)
        }
        return self.client.post(
            BASE_URL + "/auth/logout",
            headers=headers
        )
    #end def

    """
        Election
    """
    def create_election(self, params):
        """ api call to create elections"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.post(
            BASE_URL + "/elections/",
            data=dict(
                name=params["name"],
                description=params["description"],
            ),
            headers=headers
        )
    #end def

    def update_election(self, params, election_id):
        """ api call to update elections"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.put(
            BASE_URL + "/elections/" + election_id,
            data=dict(
                name=params["name"],
                description=params["description"],
            ),
            headers=headers
        )
    #end def

    def remove_election(self, election_id):
        """ api call to remove elections"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.delete(
            BASE_URL + "/elections/" + election_id,
            headers=headers
        )
    #end def

    def get_election(self, election_id):
        """ api call to get single election """
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.get(
            BASE_URL + "/elections/" + election_id,
            headers=headers
        )
    #end def

    def get_elections(self):
        """ api call to get all election available """
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.get(
            BASE_URL + "/elections/",
            headers=headers
        )
    #end def

    """
        Candidates
    """
    def create_candidate(self, params, election_id):
        """ api call to create candidates"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.post(
            BASE_URL + "/elections/" + election_id + "/candidates/",
            data=dict(
                name=params["name"],
                description=params["description"],
                order_no="1"
            ),
            headers=headers
        )
    #end def

    def update_candidate(self, params, election_id, candidate_id):
        """ api call to update candidates"""
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.put(
            BASE_URL + "/elections/" + election_id + "/candidates/" +
            candidate_id,
            data=dict(
                name=params["name"],
                description=params["description"],
            ),
            headers=headers
        )
    #end def

    def get_candidate(self, election_id, candidate_id):
        """ api call to get candidate information """
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.get(
            BASE_URL + "/elections/" + election_id + "/candidates/" +
            candidate_id,
            headers=headers
        )
    #end def

    def remove_candidate(self, election_id, candidate_id):
        """ api call to remove candidate """
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.delete(
            BASE_URL + "/elections/" + election_id + "/candidates/" +
            candidate_id,
            headers=headers
        )
    #end def

    def get_candidates(self, election_id):
        """ api call to get all candidate information for specific election """
        headers = {
            "Authorization" : "Bearer {}".format(self._token)
        }
        return self.client.get(
            BASE_URL + "/elections/" + election_id + "/candidates/",
            headers=headers
        )
    #end def
