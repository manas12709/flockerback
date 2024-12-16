from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource
from model.vote import Vote
from model.post import Post
from model.user import User

# Initialize the Flask application
app = Flask(__name__)

# Blueprint setup
# - Used to modularize application files
# - Registered to the Flask app
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')

# API setup
# - Connects the Api object to the Blueprint object
# - Defines the API endpoints
# - Maps objects to code containing the actions for the API
api = Api(leaderboard_api)

class LeaderboardAPI:
    """
    LeaderboardAPI class
    - Defines the API endpoint for the Leaderboard
    """
    class _Leaderboard(Resource):
        def get(self):
            """
            GET method for retrieving leaderboard data
            - Fetches all posts from the database
            - Calculates the net vote count for each post
            - Returns the leaderboard data as a JSON response
            """
            # Fetch all posts from the database
            posts = Post.query.all()
            post_vote_counts = []

            # Iterate through each post to calculate vote counts
            for post in posts:
                # Fetch the user who created the post
                user = User.query.filter_by(id=post.user_id).first()
                # Fetch all votes for the post
                votes = Vote.query.filter_by(_post_id=post.id).all()
                # Calculate the number of upvotes and downvotes
                upvotes = len([vote for vote in votes if vote._vote_type == 'upvote'])
                downvotes = len([vote for vote in votes if vote._vote_type == 'downvote'])
                # Calculate the net vote count
                net_vote_count = upvotes - downvotes

                # Append the post data to the leaderboard list
                post_vote_counts.append({
                    'post_id': post.id,
                    'post_title': post.title,
                    'user_id': user.id,
                    'username': user.username,
                    'upvotes': upvotes,
                    'downvotes': downvotes,
                    'net_vote_count': net_vote_count
                })

            # Return the leaderboard data as a JSON response
            return jsonify(post_vote_counts)

# Map the _Leaderboard class to the API endpoint for /leaderboard
api.add_resource(LeaderboardAPI._Leaderboard, '/leaderboard')

# Register the Blueprint with the Flask app
app.register_blueprint(leaderboard_api)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)