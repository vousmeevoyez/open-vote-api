"""
    Vote Services
"""
#pylint: disable=bad-whitespace
import uuid

from app.api import db

from app.api.models import *

# exceptions
from sqlalchemy.exc import IntegrityError

# http response
from app.api.http_response import created
from app.api.http_response import no_content
from app.api.http_response import ok

# socket
from app.api import socket
from app.api.election.stream import current_vote

# exceptions
from app.api.error.http import *

# utility
from app.api.utility.utils import string_to_uuid
from app.api.utility.utils import remove

from app.config import config

ERROR = config.Config.ERROR

class VoteServices:
    """ Candidate Services Class"""

    def __init__(self, user_id):
        user_record = User.query.filter_by(id=string_to_uuid(user_id), status=1).first()
        if user_record is None:
            raise RequestNotFound(ERROR["USER_NOT_FOUND"]["TITLE"],
                                  ERROR["USER_NOT_FOUND"]["MESSAGE"])
        #end if

        self._user = user_record
    #end def

    def cast(self, candidate_id):
        """ cast a vote """
        candidate = Candidate.query.filter_by(id=string_to_uuid(candidate_id), status=1).first()
        if candidate is None:
            raise RequestNotFound(ERROR["CANDIDATE_NOT_FOUND"]["TITLE"],
                                  ERROR["CANDIDATE_NOT_FOUND"]["MESSAGE"])
        #end if

        # make sure the user hasnt vote
        current_election_id = candidate.election_id
        votes = Vote.query.filter_by(user_id=self._user.id).all()

        if not votes:
            for vote in votes:
                past_voted_election_id =  vote.candidate.election_id

                if current_election_id == past_voted_election_id:
                    raise UnprocessableEntity(ERROR["ALREADY_VOTE"]["TITLE"],
                                              ERROR["ALREADY_VOTE"]["MESSAGE"])
                #end if

        try:
            vote = Vote(user_id=self._user.id, candidate_id=candidate.id)
            db.session.add(vote)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
        #end try

        # get current vote
        votes = current_vote(str(candidate.election_id))
        # send broadcast
        socket.emit("live_count", votes, broadcast=True, namespace="/stream")

        return no_content()
    #end def

    @staticmethod
    def count(candidate_id):
        """" show current vote for specific candidates """
        votes = \
        Vote.query.filter_by(candidate_id=string_to_uuid(candidate_id)).count()
        return ok({"count" : votes})
    #end def
