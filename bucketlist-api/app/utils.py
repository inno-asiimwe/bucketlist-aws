"""Module for decorated functions"""
from functools import wraps
from flask import request, jsonify, make_response
from .models import User


def auth_required(func):
    """decorator for authenticating a user using token based authentication """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """ Decorated function for authenticating a user"""
        response = {
            'status': 'Failed',
            'message': 'Invalid token'
        }
        code = 401

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            auth_token = ''
        else:
            auth_token = auth_header.split(" ")[1]
            resp = User.decode_auth_token(auth_token)
        if not auth_token or isinstance(resp, str):
            return make_response(jsonify(response)), code
        user = {'user_id': resp, 'auth_token': auth_token}
        return func(user, *args, **kwargs)
    return decorated_function


def validate_fields(field1, field2):
    """Passing arguments to decorator"""
    def check_data(func):
        """Decorator for validating fields in the request"""
        @wraps(func)
        def validate_input_data(*args, **kwargs):
            """Decorated function for validating bucketlist/item data"""
            data = request.data
            if not data or field1 not in data \
                    or field2 not in data:
                return make_response(
                    jsonify({
                        'message': 'Invalid payload'
                        })
                    ), 400
            return func(*args, **kwargs)
        return validate_input_data
    return check_data
