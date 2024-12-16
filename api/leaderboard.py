from flask import Flask, Blueprint, jsonify, request, g
from flask_restful import Api, Resource
from functools import wraps
from model.vote import Vote
from model.post import Post
from model.user import User

app = Flask(__name__)

leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

# Dummy token for demonstration purposes
VALID_TOKEN = "your_secure_token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != VALID_TOKEN:
            return jsonify({'message': 'Token is missing or invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

class LeaderboardAPI:
    class _Leaderboard(Resource):
        @token_required
        def get(self):
            posts = Post.query.all()
            post_vote_counts = []
            user_engagement = {}
            top_interests = {}

            for post in posts:
                user = User.query.filter_by(id=post.user_id).first()
                votes = Vote.query.filter_by(_post_id=post.id).all()
                upvotes = len([vote for vote in votes if vote._vote_type == 'upvote'])
                downvotes = len([vote for vote in votes if vote._vote_type == 'downvote'])
                net_vote_count = upvotes - downvotes

                post_vote_counts.append({
                    'post_id': post.id,
                    'post_title': post.title,
                    'user_id': user.id,
                    'username': user.username,
                    'upvotes': upvotes,
                    'downvotes': downvotes,
                    'net_vote_count': net_vote_count
                })

                # Track user engagement
                if user.username not in user_engagement:
                    user_engagement[user.username] = 0
                user_engagement[user.username] += 1

                # Track top interests
                if post.title not in top_interests:
                    top_interests[post.title] = 0
                top_interests[post.title] += 1

            # Sort the posts by net vote count in descending order
            post_vote_counts.sort(key=lambda x: x['net_vote_count'], reverse=True)

            # Sort user engagement and top interests
            sorted_user_engagement = sorted(user_engagement.items(), key=lambda x: x[1], reverse=True)
            sorted_top_interests = sorted(top_interests.items(), key=lambda x: x[1], reverse=True)

            return jsonify({
                'posts': post_vote_counts,
                'user_engagement': sorted_user_engagement,
                'top_interests': sorted_top_interests
            })

api.add_resource(LeaderboardAPI._Leaderboard, '/leaderboard')
app.register_blueprint(leaderboard_api)

if __name__ == '__main__':
    app.run(debug=True)