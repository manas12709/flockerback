from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.poll import Poll

# Blueprint for Poll API
poll_api = Blueprint('poll_api', __name__, url_prefix='/api')
api = Api(poll_api)

class PollAPI:
    """
    Define the API endpoints for the Poll model.
    """

    class _Read(Resource):
        """
        GET request handler: Read all polls.
        """
        def get(self):
            try:
                # Retrieve all poll records
                polls = Poll.query.all()
                # Convert each poll to a dictionary
                response_data = [poll.read() for poll in polls]
                return jsonify(response_data)
            except Exception as e:
                print(f"Poll Read Error: {e}")
                return {'message': f'Error retrieving poll data: {e}'}, 400

    class _Create(Resource):
        """
        POST request handler: Create a new poll.
        """
        def post(self):
            try:
                data = request.get_json()
                name = data.get('name')
                interests = data.get('interests')

                # Basic validation
                if not name or interests is None:
                    return {'message': 'name and interests fields are required.'}, 400

                # Create and save the new Poll
                new_poll = Poll(name, interests)
                new_poll.create()

                return {'message': 'Poll data inserted successfully'}, 201

            except Exception as e:
                print(f"Poll Create Error: {e}")
                return {'message': f'Error inserting poll data: {e}'}, 400

# Map the resources to their endpoints
api.add_resource(PollAPI._Read, '/poll_read')   # GET -> read all polls
api.add_resource(PollAPI._Create, '/poll_add')  # POST -> create new poll
