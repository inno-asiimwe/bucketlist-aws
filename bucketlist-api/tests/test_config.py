# """Module contains tests for the app configurations"""
# import unittest
# from flask import current_app
# from flask_testing import TestCase
# from app import create_app


# class TestDevelopmentConfig(TestCase):
#     """Class to test development configurations"""
#     def create_app(self):
#         """Creating a development app"""
#         app = create_app(config_name='development')
#         return app

#     def test_app_is_development(self):
#         """
#         Method ensures app is using development configurations
#         Running in debug mode
#         Using the bucketlist_api database and secret
#         """
#         self.assertEqual(self.app.config['SECRET'], 'My-secret-a-long-string')
#         self.assertTrue(self.app.config['DEBUG'])
#         self.assertFalse(current_app is None)
#         self.assertTrue(
#             self.app.config['SQLALCHEMY_DATABASE_URI'] ==
#             'postgresql://localhost/flask_api'
#         )


# class TestTestingConfig(TestCase):
#     """Class to test testing configurations"""
#     def create_app(self):
#         """Creating a test app"""
#         app = create_app(config_name='testing')
#         return app

#     def test_app_is_testing(self):
#         """
#         Method ensures app is using testing configurations
#         Running in debug mode
#         Running in testing mode
#         using the test database
#         using the correcrt secret key
#         """
#         self.assertTrue(self.app.config['DEBUG'])
#         self.assertTrue(self.app.config['TESTING'])
#         self.assertFalse(current_app is None)
#         self.assertTrue(self.app.config['SECRET'] == 'My-secret-a-long-string')
#         self.assertTrue(
#             self.app.config['SQLALCHEMY_DATABASE_URI'] ==
#             'postgresql://localhost/test_db'
#             )


# class TestStagingConfig(TestCase):
#     """Class to test the staging config"""
#     def create_app(self):
#         """Creating a staging app"""
#         app = create_app(config_name='staging')
#         return app

#     def test_app_is_staging(self):
#         """ """
#         self.assertTrue(self.app.config['DEBUG'])
#         self.assertTrue(self.app.config['SECRET'] == 'My-secret-a-long-string')
#         self.assertTrue(
#             self.app.config['SQLALCHEMY_DATABASE_URI'] ==
#             'postgresql://localhost/flask_api')


# class TestProductionConfig(TestCase):
#     """Class to test Production configurations"""
#     def create_app(self):
#         """creating a production app"""
#         app = create_app(config_name='production')
#         return app

#     def test_app_is_production(self):
#         """ """
#         self.assertFalse(self.app.config['DEBUG'])
#         self.assertFalse(self.app.config['TESTING'])
#         self.assertTrue(self.app.config['SECRET'] == 'My-secret-a-long-string')
        # self.assertTrue(
        #     self.app.config['SQLALCHEMY_DATABASE_URI'] ==
        #     'postgresql://localhost/flask_api')
