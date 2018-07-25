"""Module contains the base Test class for the app"""
from flask_testing import TestCase
from app import db, create_app


class BaseTestCase(TestCase):
    """Parent class for our test cases"""

    def create_app(self):
        """Method creates app for testing purposes"""
        app = create_app(config_name='testing')
        return app

    def setUp(self):
        """Method executed before every test to setup the test database"""
        db.create_all()
        db.session.commit()

    def tearDown(self):
        """
        Method executed at the end of every test
        so as to clear the database for the next test
        """
        db.session.remove()
        db.drop_all()
