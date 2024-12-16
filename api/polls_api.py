from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for the polls API
polls_api = Blueprint('polls_api', __name__, url_prefix='/api')
api = Api(polls_api)

# Database setup (using Flask-SQLAlchemy)
db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Define the Poll model
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(100), nullable=False)

# Polls API
class PollsAPI:
    # Define the API endpoints for polls

    class _Polls(Resource):
        def get(self):
            """Retrieve all poll responses."""
            try:
                polls = Poll.query.all()
                return jsonify({'polls': [poll.choice for poll in polls]})
            except SQLAlchemyError as e:
                return jsonify({'message': f'Error retrieving polls: {str(e)}'}), 500

        def post(self):
            """Store a new poll response."""
            data = request.get_json()
            choice = data.get('choice')
            if not choice:
                return {'message': 'Poll choice is required.'}, 400
            try:
                new_poll = Poll(choice=choice)
                db.session.add(new_poll)
                db.session.commit()
                return {'message': 'Poll choice recorded successfully'}, 201
            except SQLAlchemyError as e:
                db.session.rollback()
                return {'message': f'Failed to record poll choice: {str(e)}'}, 500

    # Add the resource for /polls
    api.add_resource(_Polls, '/polls')

    # Define a new endpoint for fetching poll statistics
    class _PollStats(Resource):
        def get(self):
            """Fetch statistics for poll responses."""
            try:
                stats = db.session.query(Poll.choice, db.func.count(Poll.choice)).group_by(Poll.choice).all()
                stats_dict = {choice: count for choice, count in stats}
                return jsonify({'poll_stats': stats_dict})
            except SQLAlchemyError as e:
                return jsonify({'message': f'Error retrieving poll statistics: {str(e)}'}), 500

    # Add the resource for /polls/stats
    api.add_resource(_PollStats, '/polls/stats')

# Helper to initialize the database
def init_db(app):
    """Initialize the database schema."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Example of registering the Blueprint and initializing the database
# (This code would typically go in the main Flask application file)