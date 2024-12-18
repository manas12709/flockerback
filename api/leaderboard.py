from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
from functools import wraps
from sqlalchemy import func
from model.vote import Vote
from model.post import Post
from model.user import User
from model.time_spent import TimeSpent
from sqlalchemy.exc import SQLAlchemyError

# Initialize the Flask application.
app = Flask(__name__)

# Create a Blueprint for the leaderboard API.
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

# Define a token for simplicity (update for production).
VALID_TOKEN = "your_secure_token"  # Replace with your secure token

# Define a decorator to require token authentication.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != VALID_TOKEN:
            return jsonify({'message': 'Unauthorized!'}), 403
        return f(*args, **kwargs)
    return decorated

class LeaderboardAPI:
    # Top Posts by Net Votes
    class _TopPosts(Resource):
        @token_required
        def get(self):
            try:
                # Fetch vote data from the Vote model
                posts_votes = Vote.query.with_entities(
                    Vote._post_id, Vote._vote_type
                ).all()

                vote_counts = {}
                for post_id, vote_type in posts_votes:
                    if post_id not in vote_counts:
                        vote_counts[post_id] = {'upvote': 0, 'downvote': 0}
                    vote_counts[post_id][vote_type] += 1

                sorted_posts = sorted(
                    vote_counts.items(),
                    key=lambda item: item[1]['upvote'] - item[1]['downvote'],
                    reverse=True
                )[:10]

                response = []
                for post_id, votes in sorted_posts:
                    net_votes = votes['upvote'] - votes['downvote']
                    post = Post.query.get(post_id)
                    user = User.query.get(post.user_id)

                    if post and user:
                        response.append({
                            "post_id": post_id,
                            "post_title": post.title,
                            "username": user.username,
                            "net_vote_count": net_votes
                        })

                return jsonify({"top_posts": response})
            except SQLAlchemyError as e:
                return jsonify({'message': f'Error retrieving top posts: {str(e)}'}), 500

    # Top Users by Time Spent
    class _TopUsers(Resource):
        @token_required
        def get(self):
            try:
                # Query to get users with the most time spent on the platform
                top_users = TimeSpent.query.with_entities(
                    TimeSpent.user_id,
                    func.sum(TimeSpent.time_spent).label('total_time')
                ).group_by(TimeSpent.user_id).order_by(func.sum(TimeSpent.time_spent).desc()).limit(10).all()

                response = []
                for user_id, total_time in top_users:
                    user = User.query.get(user_id)
                    if user:
                        response.append({
                            "user_id": user_id,
                            "username": user.username,
                            "total_time_spent": total_time
                        })

                return jsonify({"top_users": response})
            except SQLAlchemyError as e:
                return jsonify({'message': f'Error retrieving top users: {str(e)}'}), 500

    # Top Interests
    class _TopInterests(Resource):
        @token_required
        def get(self):
            try:
                # Query all users and count their interests
                users = User.query.all()
                interest_counts = {}

                for user in users:
                    interests = user.interests.split(", ")
                    for interest in interests:
                        interest_counts[interest] = interest_counts.get(interest, 0) + 1

                sorted_interests = sorted(
                    interest_counts.items(), key=lambda x: x[1], reverse=True
                )[:10]

                response = [{"interest": interest, "count": count} for interest, count in sorted_interests]

                return jsonify({"top_interests": response})
            except SQLAlchemyError as e:
                return jsonify({'message': f'Error retrieving interests: {str(e)}'}), 500

# Add resources to the API
api.add_resource(LeaderboardAPI._TopPosts, '/leaderboard/top_posts')
api.add_resource(LeaderboardAPI._TopUsers, '/leaderboard/top_users')
api.add_resource(LeaderboardAPI._TopInterests, '/leaderboard/top_interests')

# Register the blueprint
app.register_blueprint(leaderboard_api)

if __name__ == '__main__':
    app.run(debug=True, port=4887)
