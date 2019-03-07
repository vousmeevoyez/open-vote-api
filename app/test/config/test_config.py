""" 
    Test Configuration
"""
import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.config import config

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object(config.CONFIG_BY_NAME["dev"])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == \
            'postgresql://evote:passsword@localhost/db_vote_dev')


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(config.CONFIG_BY_NAME["test"])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == \
            'postgresql://evote:passsword@localhost/db_vote_testing')


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(config.CONFIG_BY_NAME["prod"])
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == \
            'postgresql://evote:passsword@localhost/db_vote_prod')

if __name__ == '__main__':
    unittest.main()
