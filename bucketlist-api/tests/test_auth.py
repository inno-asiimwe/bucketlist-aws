"""The module contains tests for the authentication service"""
import json
import time
from .base import BaseTestCase


class TestAuth(BaseTestCase):
    """Class contains tests to test the authentication service"""

    def test_register_success(self):
        """
        Tests successful registration,
        status code should be 201,
        with a success message
        """
        with self.client:
            response = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Successfully registered!', data['message'])
            self.assertIn('Success', data['status'])

    def test_register_invalid_payload(self):
        """
        Tests user registration with invalid payload,
        status code should be 400,
        with a Failed message
        """
        with self.client:
            response = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid Payload', data['message'])
            self.assertIn('Failed', data['status'])

    def test_register_duplicate(self):
        """Tests registration of a duplicate username, """
        with self.client:
            self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json'
                )
            response = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Jane',
                    lastname='Basemera',
                    username='inno',
                    password='yyy',
                    email='j@jane.com'
                )),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 409)
            self.assertIn(
                'Failed to register, duplicate user',
                data['message'])
            self.assertIn('Failed!!', data['status'])

    def test_login_success(self):
        """Tests a successful login"""
        with self.client:
            res = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        response = self.client.post(
            '/v1/auth/login',
            data=json.dumps(dict(
                username='inno',
                password='pass'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Succesfully logged in', data['message'])
        self.assertIn('Success', data['status'])
        self.assertTrue(data['auth_token'])

    def test_login_invalid_payload(self):
        """Tests a successful login"""
        with self.client:
            res = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        response = self.client.post(
            '/v1/auth/login',
            data=json.dumps(dict(
                username='inno'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])

    def test_login_unregistered(self):
        """Tests an unregistered user cannot login"""
        with self.client:
            response = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    username='unknown',
                    password='unknown'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                "Failed to login, unknown username or password",
                data['message'])
            self.assertIn('Failed', data['status'])

    def test_login_wrong_password(self):
        """Tests user cannot login in with wrong password"""
        with self.client:
            res = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                    )),
                content_type='application/json'
            )
            self.assertEqual(res.status_code, 201)
            response = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    username='inno',
                    password='wrongpass'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                "Failed to login, unknown username or password",
                data['message'])
            self.assertIn('Failed', data['status'])

    def test_reset_password_success(self):
        """Tests a successful reset of the password"""
        with self.client:
            res_register = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='Innocent',
                    lastname='Asiimwe',
                    username="inno",
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/v1/auth/reset-password',
                data=json.dumps(dict(
                    username='inno',
                    old_password='pass',
                    new_password='newpass'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Successfully changed password', data['message'])
            self.assertIn('Success', data['status'])

    def test_reset_password_unknownuser(self):
        """Tests failure in case of unregistered user"""
        with self.client:
            response = self.client.post(
                '/v1/auth/reset-password',
                data=json.dumps(dict(
                    username='inno',
                    old_password='pass',
                    new_password='newpass'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'Failed to reset password, bad username or password',
                data['message'])
            self.assertIn('Failed', data['status'])

    def test_reset_password_wrongpassword(self):
        """Tests failure incase of wrong password"""
        with self.client:
            res_register = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='inno',
                    lastname='asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )

            response = self.client.post(
                '/v1/auth/reset-password',
                data=json.dumps(dict(
                    username='inno',
                    old_password='password',
                    new_password='newpass'
                )),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(response.status_code, 401)
            self.assertIn(
                'Failed to reset password, bad username or password',
                data['message'])
            self.assertIn('Failed', data['status'])

    def test_logout_success(self):
        """Tests a logged in user can successfully"""
        with self.client:
            res_register = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='inno',
                    lastname='asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )

            res_login = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    username='inno',
                    password='pass'
                )),
                content_type='application/json'
            )

            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(
                        res_login.data.decode()
                        )['auth_token']
                    )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Successfully logged out', data['message'])
            self.assertIn('Success', data['status'])

    def test_logout_expired_token(self):
        """Tests failure incase the auth_token has expired"""
        with self.client:
            res_register = self.client.post(
                '/v1/auth/register',
                data=json.dumps(dict(
                    firstname='inno',
                    lastname='asiimwe',
                    username='inno',
                    password='pass',
                    email='asiimwe@outlook.com'
                )),
                content_type='application/json'
            )

            res_login = self.client.post(
                '/v1/auth/login',
                data=json.dumps(dict(
                    username='inno',
                    password='pass'
                )),
                content_type='application/json'
            )

            time.sleep(6)

            response = self.client.post(
                '/v1/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(
                        res_login.data.decode()
                        )['auth_token']
                    )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 401)
            self.assertIn("Invalid token", data['message'])
            self.assertIn("Failed", data['status'])
