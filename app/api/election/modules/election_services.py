"""
    Election Services
"""
#pylint: disable=bad-whitespace
import uuid

from app.api import db

from app.api.models import Election

# exceptions
from sqlalchemy.exc import IntegrityError

from app.api.serializer import ElectionSchema

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

class ElectionServices:
    """ Election Services Class"""

    def __init__(self, key):
        election = Election.query.filter_by(id=string_to_uuid(key), status=1).first()
        if election is None:
            raise RequestNotFound(ERROR["ELECTION_NOT_FOUND"]["TITLE"],
                                  ERROR["ELECTION_NOT_FOUND"]["MESSAGE"])
        #end if
        self.election = election
    #end def

    @staticmethod
    def add(election, filename):
        """ add user """
        try:
            # assign foreign key
            election.images = filename

            db.session.add(election)
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise DuplicateElection(error)
        #end try
        response = {
            "election_id" : str(election.id)
        }
        return created(response)
    #end def

    @staticmethod
    def show_all():
        """ show all available election """
        election = Election.query.filter_by(status=1).all()
        election_list = ElectionSchema(many=True).dump(election).data
        return ok(election_list)
    #end def

    def info(self):
        """ show election info"""
        election_info = ElectionSchema().dump(self.election).data
        return ok(election_info)
    #end def

    def update(self, params):
        """ update election """
        self.election.name        = params["name"]
        self.election.description = params["description"]

        # remove the previous image first and the upload a new one
        result = remove(self.election.images)
        self.election.images = params["images"]

        db.session.commit()
        return no_content()
    #end def

    def remove(self):
        """ remove election """
        db.session.delete(self.election)
        db.session.commit()
        return no_content()
    #end def
