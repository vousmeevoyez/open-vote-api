"""
    Election Integration Testing Between Routes & Services
"""
import json

from app.test.base  import BaseTestCase

class TestElectionRoutes(BaseTestCase):

    def test_create_election(self):
        """ test api call to create election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)

    def test_update_election(self):
        """ test api call to update election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.update_election({
            "name"       : "some leection name",
            "description": "some election description"
        }, election_id)
        self.assertEqual(result.status_code, 204)

    def test_remove_election(self):
        """ test api call to remove election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.remove_election(election_id)
        self.assertEqual(result.status_code, 204)

    def test_get_election(self):
        """ test api call to get election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.get_election(election_id)
        self.assertEqual(result.status_code, 200)

    def test_get_elections(self):
        """ test api call to get election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.get_elections()
        self.assertEqual(result.status_code, 200)

    def test_create_candidates(self):
        """ test api call to create candidates for specific election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)

    def test_update_candidate(self):
        """ test api call to create candidates for specific election and update
        the information"""
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        candidate_id = response["data"]["candidate_id"]

        result = self.update_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id, candidate_id)
        self.assertEqual(result.status_code, 204)

    def test_get_candidate(self):
        """ test api call to create candidates for specific election and get 
        the information"""
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        candidate_id = response["data"]["candidate_id"]

        result = self.get_candidate(election_id, candidate_id)
        self.assertEqual(result.status_code, 200)

    def test_get_candidates(self):
        """" get all candidates for specific election """
        result = self.create_election({
            "name"       : "some leection name",
            "description": "some election description"
        })
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        election_id = response["data"]["election_id"]

        result = self.create_candidate({
            "name"       : "some candidate name",
            "description": "some canddiate description"
        }, election_id)
        self.assertEqual(result.status_code, 201)
        response = result.get_json()
        candidate_id = response["data"]["candidate_id"]

        result = self.get_candidates(election_id)
        self.assertEqual(result.status_code, 200)
