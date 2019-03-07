"""
    Request Schema
"""
from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

class ApiKeyRequestSchema:
    """Define all mandatory argument for creating api key"""
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True)
    parser.add_argument("email",type=str, required=True)
#end class

class ClientRequestSchema:
    """Define all mandatory argument for creating client"""
    parser = reqparse.RequestParser()
    parser.add_argument("client_name", type=str, required=True)
    parser.add_argument("client_uri",type=str, required=True)
    parser.add_argument("scope",type=str, required=True)
    parser.add_argument("redirect_uri",type=str, required=True)
    parser.add_argument("grant_type",type=str, required=True)
    parser.add_argument("response_type",type=str, required=True)
    parser.add_argument("token_endpoint_auth_method",type=str, required=True)
#end class

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
    parser.add_argument("images",type=FileStorage, location="files", required=True)
    parser.add_argument("description",type=str, required=True)
#end class
