"""
    Base Test
"""
from flask_testing  import TestCase

from manage  import app
from app.api import db
# configuration
from app.config import config
# models

TEST_CONFIG = config.TestingConfig

class BaseTestCase(TestCase):
    """ This is Base Tests """

    def create_app(self):
        app.config.from_object(TEST_CONFIG)
        return app

    def setUp(self):
        db.create_all()
        # wrap everything for initialization here
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
