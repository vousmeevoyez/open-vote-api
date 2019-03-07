from app.test.base      import BaseTestCase
from app.api.serializer import *
from app.api.models     import *
from app.config     import config

from marshmallow import ValidationError


class TestApiKeySchema(BaseTestCase):

    def test_validate_name_too_short(self):
        """ test api key serializer with too short string"""
        data = {
            "name" : "i",
            "email" : "jennie@modana.id"
        }
        with self.assertRaises(ValidationError):
            api_key = ApiKeySchema(strict=True).load(data)

    def test_validate_name_too_long(self):
        """ test api key serializer with too long string"""
        data = {
            "name" :
            "jaskldjlkasjdkljaslkjdlkajsldjlasjdljalksjdlkajslkdjakslaljdlasjldjsaljdlsaj",
            "email" : "jennie@modana.id"
        }
        with self.assertRaises(ValidationError):
            api_key = ApiKeySchema(strict=True).load(data)

    def test_validate_name_invalid(self):
        """ test api key serializer with too long string"""
        data = {
            "name" : "&@!*^@*&!^*@^*!^@^!*",
            "email" : "jennie@modana.id"
        }
        with self.assertRaises(ValidationError):
            api_key = ApiKeySchema(strict=True).load(data)

    def test_validate_email_invalid(self):
        """ test api key serializer with invalid email"""
        data = {
            "name" : "jennie",
            "email" : "jennie!modana.id"
        }
        with self.assertRaises(ValidationError):
            api_key = ApiKeySchema(strict=True).load(data)

class TestUserSchema(BaseTestCase):

    def test_validate_username_too_short(self):
        """ test user serializer with too short string"""
        data = {
            "username"    : "i",
            "name"        : "Jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_username_too_long(self):
        """ test user serializer with too long string"""
        data = {
            "username"    :
            "dsaklhkjsahkdhjakshdkahskjdhjkahskjdhjkashdjklhasjhhdksahklasdhklsah",
            "name"        : "Jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_username_invalid(self):
        """ test user serializer with invalid string"""
        data = {
            "username"    : "^@*&!^&*@!^*&^!&*@^*@!^",
            "name"        : "Jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_name_too_short(self):
        """ test user serializer with too short string"""
        data = {
            "username"    : "jennei",
            "name"        : "s",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)


    def test_validate_name_too_long(self):
        """ test user serializer with too long string"""
        data = {
            "username"    : "jennei",
            "name"        :
            "asdjhaslkdjlkasjdlkjalksjdljasljdlajsldjlasjldsaasjdlsajldjasljlskjdsljdksljkldjklsjdjsljdsjkldsjkldjsljdlsjldsjlkjslkdjlsjdljsljdlsjldsda",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_name_invalid(self):
        """ test user serializer with invalid string"""
        data = {
            "username"    : "jennei",
            "name"        : "&*&@!*!@*&^@!&*^",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_identity_too_short(self):
        """ test user serializer with short identity_id"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_identity_too_short(self):
        """ test user serializer with short identity_id"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1000000000000000000000000000",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_identity_too_short(self):
        """ test user serializer with short identity_id"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "asdasdasdsaas",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_msisdn_invalid(self):
        """ test user serializer with invalid phoen number"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "0812123",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_email_invalid(self):
        """ test user serializer with invalid email"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie!modana.id",
            "password"    : "password",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_password(self):
        """ test user serializer with invalid password"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "pas",
            "role"        : "ADMIN",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)

    def test_validate_role(self):
        """ test user serializer with invalid role"""
        data = {
            "username"    : "jennei",
            "name"        : "jennie",
            "identity_id" : "1111222233334444",
            "msisdn"      : "081212341234",
            "email"       : "jennie@modana.id",
            "password"    : "password",
            "role"        : "IDOL",
        }
        with self.assertRaises(ValidationError):
            api_key = UserSchema(strict=True).load(data)
