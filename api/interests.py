from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

interests_api = Blueprint('interests_api', __name__, url_prefix='/api')

api = Api(interests_api)

class InterestsAPI:
    """
    Define the API endpoints for the Interests model.
    """
    class _CRUD(Resource):
        """
        Interests API operation for Create, Read, Update, Delete.
        """

        @token_required()
        def get(self):
            """
            Return the interests of the authenticated user as a JSON object.
            """
            current_user = g.current_user
            interests = current_user.interests
            if not interests:
                return {'message': 'No interests found for this user'}, 404
            return jsonify(interests)

        @token_required()
        def post(self):
            """
            Add new interests to the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()
            new_interests = body.get('interests')
            if not new_interests:
                return {'message': 'No interests provided'}, 400

            current_user.interests = new_interests
            current_user.update()
            return jsonify(current_user.interests)

        @token_required()
        def put(self):
            """
            Update the interests of the authenticated user.
            """
            current_user = g.current_user
            body = request.get_json()
            updated_interests = body.get('interests')
            if not updated_interests:
                return {'message': 'No interests provided'}, 400

            current_user.interests = updated_interests
            current_user.update(body)
            return jsonify(current_user.interests)

        @token_required()
        def delete(self):
            """
            Delete a specified interest of the authenticated user.
            """
            body = request.get_json()

            if not body or 'interest' not in body:
                return {'message': 'No interest provided'}, 400
            
            current_user = g.current_user
            interest_to_delete = body.get('interest')
            interests = current_user.interests.split(', ')

            if interest_to_delete not in interests:
                return {'message': 'Interest not found'}, 404

            interests.remove(interest_to_delete)
            current_user.interests = ', '.join(interests)
            current_user.update({'interests': current_user.interests})

            return {'message': 'Interest deleted successfully'}, 200

api.add_resource(InterestsAPI._CRUD, '/interests')
