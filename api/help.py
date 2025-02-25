from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.help_request import HelpRequest
from __init__ import db

help_api = Blueprint('help_api', __name__, url_prefix='/api')
api = Api(help_api)

class HelpRequestAPI(Resource):
    @token_required()
    def get(self):
        """
        Retrieve all help requests.
        """
        current_user = g.current_user
        if current_user.role == 'Admin':
            help_requests = HelpRequest.query.all()
        else:
            help_requests = HelpRequest.query.filter_by(user_id=current_user.id).all()

        if not help_requests:
            return jsonify({'message': 'No help requests found'}), 404

        return jsonify([help_request.read() for help_request in help_requests])

    @token_required()
    def post(self):
        """
        Create a new help request.
        """
        current_user = g.current_user
        data = request.get_json()

        if not data or 'message' not in data:
            return {'message': 'Message is required'}, 400

        help_request = HelpRequest(message=data['message'], user_id=current_user.id)
        help_request.create()
        return jsonify(help_request.read()), 201

    @token_required()
    def put(self):
        """
        Update a help request.
        """
        current_user = g.current_user
        data = request.get_json()

        if 'id' not in data:
            return {'message': 'Help request ID is required'}, 400
        if 'message' not in data:
            return {'message': 'Help request message is required'}, 400

        help_request = HelpRequest.query.get(data['id'])
        if not help_request:
            return {'message': 'Help request not found'}, 404

        updated_help_request = help_request.update({'message': data['message'], 'response': data.get('response'), 'status': data.get('status')})
        if updated_help_request:
            return jsonify(updated_help_request.read())
        else:
            return {'message': 'Failed to update help request'}, 500

    @token_required()
    def delete(self):
        """
        Delete a help request by ID.
        """
        data = request.get_json()
        if 'id' not in data:
            return {'message': 'Help request ID is required'}, 400

        help_request = HelpRequest.query.get(data['id'])
        if not help_request:
            return {'message': 'Help request not found'}, 404

        help_request.delete()
        return {'message': 'Help request deleted'}, 200

class HelpRequestRespondAPI(Resource):
    @token_required()
    def post(self):
        """
        Respond to a help request.
        """
        current_user = g.current_user
        if current_user.role != 'Admin':
            return {'message': 'Unauthorized'}, 403

        data = request.get_json()
        if 'id' not in data or 'response' not in data:
            return {'message': 'Help request ID and response are required'}, 400

        help_request = HelpRequest.query.get(data['id'])
        if not help_request:
            return {'message': 'Help request not found'}, 404

        help_request.response = data['response']
        help_request.status = 'Responded'
        db.session.commit()
        return jsonify(help_request.read())

# Add resource endpoints
api.add_resource(HelpRequestAPI, '/help_requests')
api.add_resource(HelpRequestRespondAPI, '/help_requests/respond')

# Ensure to import and register the blueprint in your main application file