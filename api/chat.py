from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.chat import Chat

chat_api = Blueprint('chat_api', __name__, url_prefix='/api')
api = Api(chat_api)

class ChatAPI:
    """
    Define the API CRUD endpoints for the Chat model.
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new chat message.
            """
            current_user = g.current_user
            data = request.get_json()

            if not data or 'message' not in data or 'channel_id' not in data:
                return {'message': 'Message and Channel ID are required'}, 400

            chat = Chat(message=data['message'], user_id=current_user.id, channel_id=data['channel_id'])
            chat.create()
            return jsonify(chat.read())

        @token_required()
        def get(self):
            """
            Retrieve a single chat message by ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'Chat ID is required'}, 400

            chat = Chat.query.get(data['id'])
            if not chat:
                return {'message': 'Chat message not found'}, 404

            return jsonify(chat.read())

        @token_required()
        def delete(self):
            """
            Delete a chat message by ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'Chat ID is required'}, 400

            chat = Chat.query.get(data['id'])
            if not chat:
                return {'message': 'Chat message not found'}, 404

            chat.delete()
            return {'message': 'Chat message deleted'}, 200

    class _CHANNEL(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all chat messages by channel ID.
            """
            data = request.get_json()
            if 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400

            chats = Chat.query.filter_by(_channel_id=data['channel_id']).all()
            return jsonify([chat.read() for chat in chats])

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve all chat messages by channel ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Channel data not found'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID not found'}, 400
            
            # Find all chats by channel ID
            chats = Chat.query.filter_by(_channel_id=data['channel_id']).all()
            # Prepare a JSON list of all the chats, using list comprehension
            json_ready = [chat.read() for chat in chats]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)


    # Add resource endpoints
    api.add_resource(_CRUD, '/chat')
    api.add_resource(_CHANNEL, '/chats/channel')
    api.add_resource(_FILTER, '/chats/filter')
