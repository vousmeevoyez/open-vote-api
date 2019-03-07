"""
    Request Schema
"""
from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

class UserRequestSchema:
    """Define all mandatory argument for creating user"""
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("name", type=str, required=True)
    parser.add_argument("email",type=str, required=True)
    parser.add_argument("identity_id",type=str, required=True)
    parser.add_argument("msisdn",type=str, required=True)
    parser.add_argument("password",type=str, required=True)
    parser.add_argument("role",type=str, required=True)
#end class

class AuthRequestSchema:
    """Define all mandatory argument for auth user"""
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password",type=str, required=True)
#end class

class ElectionRequestSchema:
    """Define all mandatory argument for creating user"""
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True)
    parser.add_argument("images",type=FileStorage, location="files")
    parser.add_argument("description",type=str, required=True)
#end class
