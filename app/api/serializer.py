"""
    Serializer & Deserialize
"""
import re

from marshmallow import fields
from marshmallow import ValidationError
from marshmallow import validates
from marshmallow import post_load

from app.api import ma

from app.api.models import User
from app.api.models import Election
from app.api.models import Candidate

from app.config import config

ROLE = config.Config.ROLE

def cannot_be_blank(string):
    """
        function to make user not enter empty string
        args :
            string -- user inputted data
    """
    if not string:
        raise ValidationError("Data cannot be blank")
#end def

def validate_name(name):
    """
        function to validate name
        args:
            name -- name
    """
    # onyl allow alphabet character
    pattern = r"^[a-zA-Z0-9 ]+$"
    if len(name) < 2:
        raise ValidationError('Invalid name, minimum is 2 character')
    if len(name) > 70:
        raise ValidationError('Invalid name, max is 70 character')
    if  re.match(pattern, name) is None:
        raise ValidationError('Invalid name, only alphanumeric allowed')
#end def

def validate_description(description):
    """
        function to validate description
        args:
            description -- description
    """
    # onyl allow alphabet character
    pattern = r"^[a-zA-Z ]+$"
    if len(description) < 10:
        raise ValidationError('Invalid description, minimum is 10 character')
    if len(description) > 100:
        raise ValidationError('Invalid description, max is 100 character')
    if  re.match(pattern, description) is None:
        raise ValidationError('Invalid name, only alphabet allowed')
#end def

class ApiKeySchema(ma.Schema):
    """ this is class schema for Api Key"""
    id          = fields.Str(load_only=True)
    secret_key  = fields.Str()
    name        = fields.Str(required=True, validate=(cannot_be_blank, validate_name))
    email       = fields.Str(required=True, validate=cannot_be_blank)
    created_at  = fields.DateTime('%Y-%m-%d %H:%M:%S')
    status      = fields.Method("bool_to_status")

    def bool_to_status(self, obj):
        """
            function to convert boolean into human friendly string
            args:
                obj - user object
        """
        status = "ACTIVE"
        if obj.status == 0:
            status = "INACTIVE"
        return status
    #end def

    @validates('email')
    def validate_email(self, email):
        """
            function to validate email
            args:
                email -- email
        """
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
            pass
        else:
            raise ValidationError('Invalid email')
    #end def

    @post_load
    def make_object(self, request_data):
        """ create api key object """
        return ApiKey(**request_data)
    #end def

class UserSchema(ma.Schema):
    """ this is class schema for User"""
    id          = fields.Str()
    username    = fields.Str(required=True, validate=cannot_be_blank, allow_none=True)
    name        = fields.Str(required=True, validate=(cannot_be_blank, validate_name))
    identity_id = fields.Str(required=True, validate=cannot_be_blank)
    msisdn      = fields.Str(required=True, validate=cannot_be_blank)
    email       = fields.Str(required=True, validate=cannot_be_blank)
    password    = fields.Str(required=True, validate=cannot_be_blank, load_only=True)
    role        = fields.Method("role_id_to_role", validate=cannot_be_blank)
    created_at  = fields.DateTime('%Y-%m-%d %H:%M:%S')
    status      = fields.Method("bool_to_status")

    def bool_to_status(self, obj):
        """
            function to convert boolean into human friendly string
            args:
                obj - user object
        """
        status = "ACTIVE"
        if obj.status == 0:
            status = "INACTIVE"
        return status
    #end def

    def role_id_to_role(self, obj):
        """
            function to convert role id into human friendly string
            args:
                obj - user object
        """
        if obj.role == 0:
            role = "SUPERADMIN"
        elif obj.role == 1:
            role = "ADMIN"
        elif obj.role == 2:
            role = "COMMITEE"
        elif obj.role == 3:
            role = "PARTICIPANT"
        #end if
        return role
    #end def

    @validates('username')
    def validate_username(self, username):
        """
            function to validate username
            args:
                username -- username
        """
        # onyl allow alphanumeric character, . _ -
        if username is not None:
            pattern = r"^[a-zA-Z0-9_.-]+$"
            if len(username) < 1:
                raise ValidationError('Invalid username, minimum is 1 character')
            if len(username) > 32:
                raise ValidationError('Invalid username, max is 32 character')
            if  re.match(pattern, username) is None:
                raise ValidationError('Invalid username, only alphanumeric, . _ - allowed')
    #end def

    @validates('identity_id')
    def validate_identity_id(self, username):
        """
            function to validate identity_id
            args:
                identity_id -- identity_id
        """
        # onyl allow alphanumeric character, . _ -
        pattern = r"^[0-9]+$"
        if len(username) < 6:
            raise ValidationError('Invalid identity_id, minimum is 6 digit')
        if len(username) > 16:
            raise ValidationError('Invalid identity_id, max is 16 digit')
        if  re.match(pattern, username) is None:
            raise ValidationError('Invalid identity_id, only number allowed')
    #end def

    @validates('msisdn')
    def validate_msisdn(self, msisdn):
        """
            function to validate phone_number
            args:
                phone_number -- phone number
        """
        # only allow 0-9, minimal 10  and maximal is 12 digit
        pattern = r"^[0-9]{10,12}$"
        if re.search(pattern, msisdn) is None:
            raise ValidationError('Invalid msisdn')
        #end if
    #end def

    @validates('email')
    def validate_email(self, email):
        """
            function to validate email
            args:
                email -- email
        """
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
            pass
        else:
            raise ValidationError('Invalid email')
    #end def

    @validates('password')
    def validate_password(self, password):
        """
            function to validate password
            args:
                password -- password
        """
        if re.match(r'[A-Za-z0-9@#$%^&+=]{6,}', password):
            pass
        else:
            raise ValidationError("Invalid Password, Minimum 6 Character")
    #end def

    @validates('role')
    def validate_role(self, role):
        """
            function to validate role
            args:
                role -- role
        """
        pattern = r"^[a-zA-Z]+$"
        if re.match(pattern, role) is None:
            raise ValidationError("Invalid Role, only alphabet allowed")
        #end if

        if role not in ["ADMIN", "COMMITEE", "PARTICIPANT"]:
            raise ValidationError("Invalid Role")
    #end def

    @post_load
    def make_object(self, request_data):
        """ create user object """
        role = request_data["role"]
        request_data["role"] = ROLE[role]
        return User(**request_data)
    #end def

class CandidateSchema(ma.Schema):
    """ this is class schema for Election """
    id          = fields.Str()
    order_no    = fields.Str()
    name        = fields.Str(required=True, validate=(cannot_be_blank, validate_name))
    description = fields.Str(required=True, validate=(cannot_be_blank, validate_description))
    images      = fields.Str(dump_only=True)
    users       = fields.Nested(UserSchema, many=True)
    status      = fields.Method("bool_to_status")
    votes       = fields.Method("count_vote")
    created_at  = fields.DateTime('%Y-%m-%d %H:%M:%S')

    @post_load
    def make_object(self, request_data):
        """ create user object """
        return Candidate(**request_data)
    #end def

    def count_vote(self, obj):
        return len(obj.votes)

    def bool_to_status(self, obj):
        """
            function to convert boolean into human friendly string
            args:
                obj - user object
        """
        status = "ACTIVE"
        if obj.status is False:
            status = "INACTIVE"
        return status
    #end def

class ElectionSchema(ma.Schema):
    """ this is class schema for Election """
    id          = fields.Str()
    name        = fields.Str(required=True, validate=(cannot_be_blank, validate_name))
    description = fields.Str(required=True, validate=(cannot_be_blank, validate_description))
    images      = fields.Str(dump_only=True)
    status      = fields.Method("bool_to_status")
    candidates  = fields.Nested(CandidateSchema, many=True)
    created_at  = fields.DateTime('%Y-%m-%d %H:%M:%S')

    @post_load
    def make_object(self, request_data):
        """ create user object """
        return Election(**request_data)
    #end def

    def bool_to_status(self, obj):
        """
            function to convert boolean into human friendly string
            args:
                obj - user object
        """
        status = "ACTIVE"
        if obj.status is False:
            status = "INACTIVE"
        return status
    #end def
