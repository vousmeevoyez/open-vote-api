"""
    Election Services
"""
#pylint: disable=bad-whitespace
import uuid

from app.api import db

from app.api.models import Election
from app.api.models import Candidate

# exceptions
from sqlalchemy.exc import IntegrityError

from app.api.serializer import ElectionSchema
from app.api.serializer import CandidateSchema

# http response
from app.api.http_response import created
from app.api.http_response import no_content
from app.api.http_response import ok

# exceptions
from app.api.error.http import *

# utility
from app.api.utility.utils import string_to_uuid
from app.api.utility.utils import remove

from app.config import config

ERROR = config.Config.ERROR

class CandidateServices:
    """ Candidate Services Class"""

    def __init__(self, election_key, candidate_key=None):
        election_record = Election.query.filter_by(id=string_to_uuid(election_key), status=1).first()
        if election_record is None:
            raise RequestNotFound(ERROR["ELECTION_NOT_FOUND"]["TITLE"],
                                  ERROR["ELECTION_NOT_FOUND"]["MESSAGE"])
        #end if

        if candidate_key is not None:
            candidate_record = \
            Candidate.query.filter_by(id=string_to_uuid(candidate_key)).first()
            if candidate_record is None:
                raise RequestNotFound(ERROR["CANDIDATE_NOT_FOUND"]["TITLE"],
                                      ERROR["CANDIDATE_NOT_FOUND"]["MESSAGE"])
            self.candidate = candidate_record
        #end if
        self.election = election_record
    #end def

    def add(self, candidate, filename):
        """ add candidate """
        try:
            # create uuid
            # assign foreign key
            candidate.election_id = self.election.id
            candidate.images = filename

            db.session.add(candidate)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
        #end try
        response = {
            "candidate_id" : str(candidate.id)
        }
        return created(response)
    #end def

    def show_all(self):
        """ show all available candidate on specific election """
        candidates = Candidate.query.filter_by(election_id=self.election.id).all()
        candidate_list = CandidateSchema(many=True).dump(candidates).data
        return ok(candidate_list)
    #end def

    def info(self):
        """ show candidate info"""
        candidate_info = CandidateSchema().dump(self.candidate).data
        return ok(candidate_info)
    #end def

    def update(self, params):
        """ update candidate information """
        self.candidate.name        = params["name"]
        self.candidate.description = params["description"]

        # remove the previous image first and the upload a new one
        result = remove(self.candidate.images)
        self.candidate.images = params["images"]

        db.session.commit()
        return no_content()
    #end def

    def remove(self):
        """ remove election """
        db.session.delete(self.candidate)
        db.session.commit()
        return no_content()
    #end def
