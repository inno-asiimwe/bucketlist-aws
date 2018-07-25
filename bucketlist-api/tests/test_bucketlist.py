"""Module contains tests for the bucketlist service"""
import json
from app.models import User
from .base import BaseTestCase


class TestBucketlist(BaseTestCase):
    """class contains tests for the bucketlist service"""

    def register_user(
            self,
            firstname='Innocent',
            lastname='Asiimwe',
            username='inno',
            password='pass',
            email='a@a.com'):
        """Helper method to register a user"""
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'password': password,
            'email': email
        }
        response = self.client.post(
            '/v1/auth/register',
            data=json.dumps(data),
            content_type='application/json')
        return response

    def login_user(self, username='inno', password='pass'):
        """Helper method to login a user"""
        data = dict(
            username=username,
            password=password
        )
        response = self.client.post(
            '/v1/auth/login',
            data=json.dumps(data),
            content_type='application/json'
            )
        return response

    def test_create_bucketlist_success(self):
        """Tests successful creation of bucketlist"""

        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 201)
            self.assertIn('before 30', data['name'])

    def test_create_bucketlist_invalid_payload(self):
        """Tests successful creation of bucketlist"""

        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    owner=user_id
                )),
                content_type='application/json'
                )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])

    def test_create_bucketlist_duplicate_name(self):
        """Tests API doesnot create bucketlists with duplicate"""

        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            response1 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            response2 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Places to visit before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            data1 = json.loads(response1.data.decode())
            data2 = json.loads(response2.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response1.status_code, 201)
            self.assertEqual(response2.status_code, 400)
            self.assertIn('before 30', data1['name'])
            self.assertIn('Failed', data2['status'])

    def test_get_bucketlists(self):
        """Tests api can get all bucketlists for a given user  """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            response = self.client.get(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('before 30', data[0]['name'])

    def test_get_bucketlist(self):
        """Tests api can get a bucketlist by id """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            result = json.loads(res_post.data.decode())
            response = self.client.get(
                '/v1/bucketlists/{}'.format(result['id']),
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('before 30', data['name'])

    def test_get_bucketlist_invalid_id(self):
        """ Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.get(
                '/v1/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)

    def test_edit_bucketlist_success(self):
        """Tests API can update bucketlist"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            result = json.loads(res_post.data.decode())
            response = self.client.put(
                '/v1/bucketlists/{}'.format(result['id']),
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='Before thirty',
                    description='Things to do before age 30'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Before thirty', data['name'])

    def test_edit_bucketlist_invalid_id(self):
        """Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.put(
                '/v1/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before 30'
                )),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)

    def test_delete_bucketlist(self):
        """ Tests API can delete bucketlist by id """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_post = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization="Bearer " + access_token),
                data=json.dumps(dict(
                    name='before 30',
                    description='Things to do before I am 30 years',
                    owner=user_id
                )),
                content_type='application/json'
                )
            response = self.client.delete(
                '/v1/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            res_get = self.client.get(
                '/v1/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )

            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_post.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Success', data['status'])
            self.assertEqual(res_get.status_code, 404)

    def test_delete_bucketlist_invalid_id(self):
        """Tests API returns 404 for an invalid id"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            access_token = json.loads(res_login.data.decode())['auth_token']
            response = self.client.delete(
                '/v1/bucketlists/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='before 30'
                )),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(response.status_code, 404)

    def test_create_item_success(self):
        """Tests API can create an item in a bucketlist """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response.status_code, 201)
            self.assertIn('Build a rental house', data['description'])

    def test_create_item_invalid_name(self):
        """Tests API doesnot create items with the same name in a bucketlist"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response_2 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            data_2 = json.loads(response_2.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertEqual(response_2.status_code, 409)
            self.assertIn('Failed', data_2['status'])

    def test_create_item_invalid_bucketlist(self):
        """ """
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/v1/bucketlists/2/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response.status_code, 404)

    def test_edit_item_success(self):
        """Tests API can edit existing item"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/v1/bucketlists/1/items/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a home',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Build a home', data['name'])

    def test_edit_item_invalid_id(self):
        """Tests API can edit existing item"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/v1/bucketlists/2/items/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a home',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item not found', data['message'])

    def test_edit_item_duplicate_name(self):
        """Tests API can edit existing item"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30 years old',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response_2 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a school',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response = self.client.put(
                '/v1/bucketlists/1/items/1',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a school',
                    description='Build a family house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertEqual(response_2.status_code, 201)
            self.assertEqual(response.status_code, 409)
            self.assertIn('Failed', data['status'])

    def test_delete_item_success(self):
        """Test API can delete item"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response = self.client.delete(
                '/v1/bucketlists/1/items/1',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertIn('Success', data['status'])

    def test_delete_item_invalid_id(self):
        """Test API can delete item"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response_1 = self.client.post(
                '/v1/bucketlists/1/items',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Build a house',
                    description='Build a rental house',
                    bucketlist_id=1
                )),
                content_type='application/json'
            )
            response = self.client.delete(
                '/v1/bucketlists/1/items/2',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response_1.status_code, 201)
            self.assertEqual(response.status_code, 404)
            self.assertIn('Item not found', data['message'])

    def test_search_for_bucketlist(self):
        """Tests API can search for a bucketlist by name"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/v1/bucketlists?q=Before 30',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Before 30', data[0]['name'])

    def test_pagination(self):
        """Tests API can paginate results"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist2 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Tours',
                    description='The tours of my life',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist3 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 60 ',
                    description='Things to do before I am 60 years',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/v1/bucketlists?limit=2',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(res_bucketlist2.status_code, 201)
            self.assertEqual(res_bucketlist3.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(2, len(data))

    def test_search_with_pagination(self):
        """Tests API can paginate search results"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist2 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Tours Before 90',
                    description='The tours of my life',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist3 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 60 ',
                    description='Things to do before I am 60 years',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/v1/bucketlists?page=1&limit=2&q=Before',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(res_bucketlist2.status_code, 201)
            self.assertEqual(res_bucketlist3.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(2, len(data['items']))

    def test_pagination_page_access(self):
        """Tests API can paginate results"""
        with self.client:
            res_register = self.register_user()
            res_login = self.login_user()
            user_id = User.query.filter_by(username='inno').first().id
            access_token = json.loads(res_login.data.decode())['auth_token']
            res_bucketlist = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 30',
                    description='Things to do before I am 30',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist2 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Tours',
                    description='The tours of my life',
                    owner=user_id
                )),
                content_type='application/json'
            )
            res_bucketlist3 = self.client.post(
                '/v1/bucketlists',
                headers=dict(Authorization='Bearer ' + access_token),
                data=json.dumps(dict(
                    name='Before 60 ',
                    description='Things to do before I am 60 years',
                    owner=user_id
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/v1/bucketlists?page=1&limit=2',
                headers=dict(Authorization='Bearer ' + access_token),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(res_register.status_code, 201)
            self.assertEqual(res_login.status_code, 200)
            self.assertEqual(res_bucketlist.status_code, 201)
            self.assertEqual(res_bucketlist2.status_code, 201)
            self.assertEqual(res_bucketlist3.status_code, 201)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(2, len(data['items']))
           
