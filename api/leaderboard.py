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
                # Get the current user ID from the request arguments
                current_user_id = request.args.get('user_id')
                
                # Query the database to get the current user by ID
                current_user = User.query.get(current_user_id)
                
                # If the current user is not found, return a 404 error message
                if not current_user:
                    return {'message': 'User not found'}, 404
                
                # Split the current user's interests into a set of interests
                current_user_interests = set(current_user.interests.split(", "))
                
                # Query the database to get all users except the current user
                all_users = User.query.filter(User.id != current_user_id).all()
                
                matched_users = []
                # Iterate over all users
                for user in all_users:
                    # Split each user's interests into a set of interests
                    user_interests = set(user.interests.split(", "))
                    
                    # Find the shared interests between the current user and each user
                    shared_interests = current_user_interests.intersection(user_interests)
                    
                    # If there are shared interests, add the user to the matched users list
                    if shared_interests:
                        matched_users.append({
                            'username': user.name,
                            'shared_interests': list(shared_interests)
                        })
                
                # Sort the matched users by the number of shared interests in descending order
                # The key=lambda x: len(x['shared_interests']) part specifies that the sorting key is the length of the 'shared_interests' list
                # reverse=True means that the list will be sorted in descending order
                matched_users.sort(key=lambda x: len(x['shared_interests']), reverse=True)
                
                # Uncomment the line below to add a breakpoint for Postman API testing
                # import pdb; pdb.set_trace()
                
                # Return the matched users as a JSON response
                return jsonify({'top_users': matched_users})
            except Exception as e:
                # If there is an error, return a 500 error message
                return {'message': f'Error retrieving top users: {str(e)}'}, 500

    # Create class for top interests
    class _TopInterests(Resource):
        def get(self):
            try:
                # Get all users
                all_users = User.query.all()
                
                interest_counts = {}
                # Iterate over all users
                for user in all_users:
                    # Split each user's interests into a list of interests
                    interests = user.interests.split(", ")
                    
                    # Count the occurrences of each interest
                    for interest in interests:
                        if interest in interest_counts:
                            interest_counts[interest] += 1
                        else:
                            interest_counts[interest] = 1
                
                # Sort interests by count in descending order
                # The key=lambda x: x[1] part specifies that the sorting key is the count of each interest
                # reverse=True means that the list will be sorted in descending order
                sorted_interests = sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)
                
                # Breakpoint for Postman API testing
                # breakpoint()
                
                # Return the top interests as a JSON response
                return jsonify({'top_interests': [{'interest': interest, 'count': count} for interest, count in sorted_interests]})
            except Exception as e:
                # If there is an error, return a 500 error message
                return {'message': f'Error retrieving top interests: {str(e)}'}, 500

# Add resources to the API
api.add_resource(Leaderboard._TopUsers, '/leaderboard/top_users')
api.add_resource(Leaderboard._TopInterests, '/leaderboard/top_interests')