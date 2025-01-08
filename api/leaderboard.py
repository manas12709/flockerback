from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import func
from model.user import User
from __init__ import db

# Create blueprint for the leaderboard API
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

class Leaderboard:
    
    class _TopUsers(Resource):
        def get(self):
            try:
                # Get the current user (for simplicity, assuming user_id is passed as a query parameter)
                current_user_id = request.args.get('self._uid')
                current_user = User.query.get(self._name)
                if not current_user:
                    return {'message': 'User not found'}, 404
                
                current_user_interests = set(self._intrests.split(", "))
                
                # Get all users except the current user
                all_users = User.query.filter(self.uid != _uid).all()
                
                matched_users = []
                for user in all_users:
                    user_interests = set(_intrests.split(", "))
                    shared_interests = current_user_interests.intersection(user_interests)
                    if shared_interests:
                        matched_users.append({
                            'username': _name,
                            'shared_interests': list(shared_interests)
                        })
                
                # Sort matched users by the number of shared interests
                matched_users.sort(key=lambda x: len(x['shared_interests']), reverse=True)
                
                return jsonify({'top_users': matched_users})
            except Exception as e:
                return {'message': f'Error retrieving top users: {str(e)}'}, 500

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
                
                return jsonify({'top_interests': [{'interest': interest, 'count': count} for interest, count in sorted_interests]})
            except Exception as e:
                return {'message': f'Error retrieving top interests: {str(e)}'}, 500

# Add resources to the API
api.add_resource(Leaderboard._TopUsers, '/leaderboard/top_users')
api.add_resource(Leaderboard._TopInterests, '/leaderboard/top_interests')