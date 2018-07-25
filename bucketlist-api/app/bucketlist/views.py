"""views for bucketlist_blueprint """
import datetime
from flask import make_response, jsonify, request
from app.utils import auth_required, validate_fields
from app.models import Bucketlist, Item
from . import bucketlist_blueprint


@bucketlist_blueprint.route('', methods=['POST'])
@auth_required
@validate_fields('name', 'description')
def create_bucketlist(user):
    """create bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
      - in: "header"
        name: "Authorization"
        description: "Token of logged in user"
        required: true
        type: string
      - in: "body"
        name: "body"
        description: "Name and description of bucketlist"
        schema:
         type: "object"
         required:
          - name
          - description
         properties:
          name:
           type: "string"
          description:
           type: "string"
    responses:
        400:
            description: "Failed"
        201:
            description: "Success"
     """
    name = request.data['name']
    description = request.data['description']
    owner = user['user_id']

    try:
        new_bucketlist = Bucketlist(name, description, owner)
        new_bucketlist.save()
        response = new_bucketlist.to_json()
        return make_response(jsonify(response)), 201
    except Exception as e:
        response = {
            'status': 'Failed',
            'message': str(e)
        }
        return make_response(jsonify(response)), 400


@bucketlist_blueprint.route('', methods=['GET'])
@auth_required
def get_bucketlists(user):
    """Retrieve bucketlists
    ---
    tags:
     - "bucketlists"
    parameters:
      - in: "header"
        name: "Authorization"
        description: "Token of logged in user"
        required: true
        type: string
      - in: "body"
        name: "body"
        description: "Name and description of bucketlist"
        schema:
         type: "object"
         required:
          - name
          - description
         properties:
          name:
           type: "string"
          description:
           type: "string"
    responses:
        400:
            description: "Failed"
        200:
            description: "success"
     """
    query = request.args.get('q')
    limit = request.args.get('limit')
    page = request.args.get('page')

    if query and limit and page:
        user_bucketlists = Bucketlist.query.filter(
            Bucketlist.name.ilike("%" + query + "%"),
            Bucketlist.owner == user['user_id']
        ).paginate(int(page), int(limit), False)
        response = {
            'items': [
                bucketlist.to_json() for bucketlist in user_bucketlists.items
                ],
            'pages': user_bucketlists.pages,
            'next_page': user_bucketlists.next_num,
            'current_page': user_bucketlists.page,
            'prev_page': user_bucketlists.prev_num,
            'has_next': user_bucketlists.has_next,
            'has_prev': user_bucketlists.has_prev
        }
        return make_response(jsonify(response)), 200
    if limit and page:
        user_bucketlists = Bucketlist.query.filter_by(
            owner=user['user_id']).paginate(int(page), int(limit), False)
        response = {
            'items': [
                bucketlist.to_json() for bucketlist in user_bucketlists.items
                ],
            'pages': user_bucketlists.pages,
            'next_page': user_bucketlists.next_num,
            'current_page': user_bucketlists.page,
            'prev_page': user_bucketlists.prev_num,
            'has_next': user_bucketlists.has_next,
            'has_prev': user_bucketlists.has_prev
        }
        return make_response(jsonify(response)), 200
    if limit:
        user_bucketlists = Bucketlist.query.filter_by(
            owner=user['user_id']).limit(int(limit))
        response = [bucketlist.to_json() for bucketlist in user_bucketlists]
        return make_response(jsonify(response)), 200
    if query:
        user_bucketlists = Bucketlist.query.filter(
            Bucketlist.name.ilike("%" + query + "%"),
            Bucketlist.owner == user['user_id']
        ).all()
        response = [bucketlist.to_json() for bucketlist in user_bucketlists]
        return make_response(jsonify(response)), 200
    user_bucketlists = Bucketlist.get_all_bucketlists(user['user_id'])
    response = [bucketlist.to_json() for bucketlist in user_bucketlists]
    return make_response(jsonify(response)), 200


@bucketlist_blueprint.route('/<int:b_id>', methods=['GET'])
@auth_required
def get_bucketlist(user, b_id):
    """ Retrieve bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
     """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    if my_bucketlist:
        response = my_bucketlist.to_json()
        return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Bucketlist not Found',
        'user': user['user_id']
    }
    return make_response(jsonify(response)), 404


@bucketlist_blueprint.route('/<int:b_id>', methods=['DELETE'])
@auth_required
def delete_bucketlist(user, b_id):
    """ Delete bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
     """

    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    if my_bucketlist:
        my_bucketlist.delete()
        response = {
            'status': 'Success',
            'bucketlist': my_bucketlist.id,
            'user': user['user_id']
        }
        return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Bucketlist not found',
        'user': user['user_id']
    }
    return make_response(jsonify(response)), 404


@bucketlist_blueprint.route('/<int:b_id>', methods=['PUT'])
@auth_required
@validate_fields('name', 'description')
def edit_bucketlist(user, b_id):
    """ Edit bucketlist
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       description: "Token of logged in user"
       required: true
       type: string
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist"
       schema:
        type: "object"
        required:
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "not found"
        200:
            description: "success"
        409:
            description: "duplicates"
     """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id).first()
    name = request.data['name']
    description = request.data['description']
    if my_bucketlist:
        if my_bucketlist.name != name:
            duplicate = Bucketlist.query.filter_by(
                name_to_compare=''.join(name.lower().split()),
                owner=user['user_id']
                ).first()
            if not duplicate:
                my_bucketlist.name = name
            else:
                response = {
                    'status': 'Failed',
                    'message': 'Name already exists'
                }
                return make_response(jsonify(response)), 409
        if my_bucketlist.description != description:
            my_bucketlist.description = description
        my_bucketlist.date_modified = datetime.datetime.utcnow()
        my_bucketlist.save()
        response = my_bucketlist.to_json()
        return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Bucketlist not found',
        'user': user['user_id']
    }
    return make_response(jsonify(response)), 404


@bucketlist_blueprint.route('/<int:b_id>/items', methods=['POST'])
@auth_required
@validate_fields('name', 'description')
def create_bucketlist_item(user, b_id):
    """Create a bucketlist item
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "header"
       name: "Authorization"
       required: true
       description: "Token of logged in user"
       type: string
     - in: "body"
       name: "body"
       required: true
       description: "Name and Description of bucketlist item"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
         name:
            type: "string"
         description:
            type: "string"
    responses:
        404:
            description: "resource not found"
        400:
            description: "Failed"
        201:
            description: "success"
        409:
            description: "Failed, Duplicate Item"
    """
    my_bucketlist = Bucketlist.query.filter_by(id=b_id,
                                               owner=user['user_id']
                                               ).first()
    if my_bucketlist:
        item = Item.query.filter_by(
            bucketlist_id=b_id,
            name_to_compare=''.join(request.data['name'].lower().split())
            ).first()
        if not item:
            try:
                new_item = Item(
                    name=request.data['name'],
                    description=request.data['description'],
                    bucketlist_id=b_id)
                new_item.save()
            except Exception as error:
                response = {
                    'status': 'Failed',
                    'message': str(error)
                }
                return make_response(jsonify(response)), 400
            response = {
                'status': 'Success',
                'id': new_item.id,
                'name': new_item.name,
                'description': new_item.description,
                'bucketlist_id': new_item.bucketlist_id
            }
            return make_response(jsonify(response)), 201
        response = {
            'status': 'Failed',
            'message': 'Item already exists'
        }
        return make_response(jsonify(response)), 409
    response = {
        'status': 'Failed',
        'message': 'Bucketlist not found',
        'user': user['user_id']
    }
    return make_response(jsonify(response)), 404


@bucketlist_blueprint.route('/<int:b_id>/items', methods=['GET'])
@auth_required
def get_bucketlist_item(user, b_id):
    """Retrieve bucketlists
    ---
    tags:
     - "bucketlists"
    parameters:
      - in: "header"
        name: "Authorization"
        description: "Token of logged in user"
        required: true
        type: string
      - in: "body"
        name: "body"
        description: "Name and description of bucketlist items"
        schema:
         type: "object"
         required:
          - name
          - description
         properties:
          name:
           type: "string"
          description:
           type: "string"
    responses:
        400:
            description: "Failed"
        200:
            description: "success"
     """
    query = request.args.get('q')
    limit = request.args.get('limit')
    page = request.args.get('page')
    bucketlist = Bucketlist.query.filter_by(id=b_id,
                                            owner=user['user_id']
                                            ).first()

    if query and limit and page:
        bucketlist_items = Item.query.filter(
            Item.name.ilike("%" + query + "%"),
            Item.bucketlist_id == b_id
        ).paginate(int(page), int(limit), False)
        response = {
            'items': [
                item.to_json() for item in bucketlist_items.items
                ],
            'pages': bucketlist_items.pages,
            'next_page': bucketlist_items.next_num,
            'current_page': bucketlist_items.page,
            'prev_page': bucketlist_items.prev_num,
            'bucketlist': bucketlist.to_json(),
            'has_next': bucketlist_items.has_next,
            'has_prev': bucketlist_items.has_prev
        }
        return make_response(jsonify(response)), 200
    if limit and page:
        bucketlist_items = Item.query.filter_by(
            bucketlist_id=b_id).paginate(int(page), int(limit), False)
        response = {
            'items': [
                item.to_json() for item in bucketlist_items.items
                ],
            'pages': bucketlist_items.pages,
            'next_page': bucketlist_items.next_num,
            'current_page': bucketlist_items.page,
            'prev_page': bucketlist_items.prev_num,
            'bucketlist': bucketlist.to_json(),
            'has_next': bucketlist_items.has_next,
            'has_prev': bucketlist_items.has_prev
        }
        return make_response(jsonify(response)), 200
    if limit:
        bucketlist_items = Item.query.filter_by(
            bucketlist_id=b_id).limit(int(limit))
        response = [item.to_json() for item in bucketlist_items]
        return make_response(jsonify(response)), 200
    if query:
        bucketlist_items = Item.query.filter(
            Item.name.ilike("%" + query + "%"),
            Item.bucketlist_id == b_id
        ).all()
        response = [item.to_json() for item in bucketlist_items]
        return make_response(jsonify(response)), 200
    bucketlist_items = Item.get_all_items(b_id)
    response = [item.to_json() for item in bucketlist_items]
    return make_response(jsonify(response)), 200


@bucketlist_blueprint.route('/<int:b_id>/items/<int:i_id>', methods=['PUT'])
@auth_required
@validate_fields('name', 'description')
def edit_bucketlist_item(user, b_id, i_id):
    """"Edit and delete bucketlist item
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "headers"
       name: "Authorization"
       required: true
       type: string
       description: "Token of logged in user"
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist item"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
            name:
                type: "string"
            description:
                type: "string"
    responses:
        200:
            description: "success"
        404:
            description: "Failed"
        409:
            description: "Duplicate name"
    """
    request_data = request.data
    my_item = Item.query.filter_by(bucketlist_id=b_id, id=i_id).first()
    name = request_data['name']
    description = request_data['description']
    if my_item:
        if name and (my_item.name != name):
            duplicate = Item.query.filter_by(
                name_to_compare=''.join(request.data['name'].lower().split()),
                bucketlist_id=b_id
                ).first()
            if not duplicate:
                my_item.name = request.data['name']
            else:
                return make_response(jsonify({'status': 'Failed'})), 409
        if my_item.description != description:
            my_item.description = request.data['description']
        my_item.save()
        response = my_item.to_json()
        return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Item not found',
        'user': user['user_id']
    }
    return make_response((jsonify(response))), 404


@bucketlist_blueprint.route('/<int:b_id>/items/<int:i_id>', methods=['DELETE'])
@auth_required
def delete_bucketlist_item(user, b_id, i_id):
    """"Edit and delete bucketlist item
    ---
    tags:
     - "bucketlists"
    parameters:
     - in: "headers"
       name: "Authorization"
       required: true
       type: string
       description: "Token of logged in user"
     - in: "body"
       name: "body"
       description: "Name and description of bucketlist item"
       schema:
        type: "object"
        required:
         - name
         - description
        properties:
            name:
                type: "string"
            description:
                type: "string"
    responses:
        200:
            description: "success"
        404:
            description: "Failed"
        409:
            description: "Duplicate name"
    """

    my_item = Item.query.filter_by(bucketlist_id=b_id, id=i_id).first()

    if my_item:
        if request.method == 'DELETE':
            my_item.delete()
            response = {
                'status': 'Success',
                'user': user['user_id']
            }
            return make_response(jsonify(response)), 200
    response = {
        'status': 'Failed',
        'message': 'Item not found',
        'user': user['user_id']
    }
    return make_response((jsonify(response))), 404
