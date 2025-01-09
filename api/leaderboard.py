from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.user import User
from __init__ import db
from model.topusers import TopUser

# Create blueprint for the leaderboard API
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

# Create class for Leaderboard
class Leaderboard:
    # Create class for top users
    class _TopUsers(Resource):
        def get(self):
            try:
                # Get the current user
                current_user_id = request.args.get('user_id')
                current_user = User.query.get(current_user_id)
                if not current_user:
                    return {'message': 'User not found'}, 404
                
                current_user_interests = set(current_user.interests.split(", "))
                
                # Get all users except the current user
                all_users = User.query.filter(User.id != current_user_id).all()
                
                matched_users = []
                for user in all_users:
                    user_interests = set(user.interests.split(", "))
                    shared_interests = current_user_interests.intersection(user_interests)
                    if shared_interests:
                        matched_users.append({
                            'username': user.name,
                            'shared_interests': list(shared_interests)
                        })
                
                # Sort matched users by the number of shared interests (descending)
                matched_users.sort(key=lambda x: len(x['shared_interests']), reverse=True)
                
                return jsonify({'top_users': matched_users})
            except Exception as e:
                return {'message': f'Error retrieving top users: {str(e)}'}, 500

    # Create class for top interests
    class _TopInterests(Resource):
        def get(self):
            try:
                # Get all users
                all_users = User.query.all()
                
                interest_counts = {}
                for user in all_users:
                    interests = user.interests.split(", ")
                    for interest in interests:
                        if interest in interest_counts:
                            interest_counts[interest] += 1
                        else:
                            interest_counts[interest] = 1
                
                # Sort interests by count
                sorted_interests = sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)
                
                # Return the top interests
                return jsonify({'top_interests': [{'interest': interest, 'count': count} for interest, count in sorted_interests]})
            except Exception as e:
                return {'message': f'Error retrieving top interests: {str(e)}'}, 500

# Add resources to the API
api.add_resource(Leaderboard._TopUsers, '/leaderboard/top_users')
api.add_resource(Leaderboard._TopInterests, '/leaderboard/top_interests')