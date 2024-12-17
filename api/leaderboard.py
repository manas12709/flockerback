from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api, Resource
from functools import wraps
from model.vote import Vote
from model.post import Post
from model.user import User
from collections import Counter

app = Flask(__name__)

leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

# Token for simplicity (update for production)
VALID_TOKEN = "your_secure_token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != VALID_TOKEN:
            return jsonify({'message': 'Unauthorized!'}), 403
        return f(*args, **kwargs)
    return decorated

class LeaderboardAPI:
    class _Leaderboard(Resource):
        @token_required
        def get(self):
            """
            Retrieve leaderboard data.
            """
            try:
                # Fetch posts and compute net votes
                posts = Post.query.all()
                post_data = []
                for post in posts:
                    user = User.query.get(post.user_id)
                    if user is None:
                        continue  # Skip posts with no valid user
                    votes = Vote.query.filter_by(post_id=post.id).all()
                    upvotes = sum(1 for vote in votes if vote.vote_type == 'upvote')
                    downvotes = sum(1 for vote in votes if vote.vote_type == 'downvote')
                    net_votes = upvotes - downvotes

                    post_data.append({
                        "post_title": post.title,
                        "username": user.username,
                        "net_vote_count": net_votes
                    })

                # Top Interests Example Logic
                interests = [post.category for post in posts]  # Assuming 'category' represents interest
                interest_counts = Counter(interests).most_common()

                # Top Users Engagement Example Logic
                user_votes = Vote.query.all()
                user_engagement = Counter(vote.user_id for vote in user_votes).most_common()
                user_data = [
                    (User.query.get(user_id).username, count) for user_id, count in user_engagement
                ]

                return jsonify({
                    "posts": post_data,
                    "top_interests": interest_counts,
                    "user_engagement": user_data
                })
            except Exception as e:
                return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

api.add_resource(LeaderboardAPI._Leaderboard, '/leaderboard')
app.register_blueprint(leaderboard_api)

if __name__ == '__main__':
    app.run(debug=True, port=4887)