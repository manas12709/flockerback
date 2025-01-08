from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json
import sqlite3
from flask_cors import CORS

#original code, not copied from templates/mr. mort/ChatGPT

# Create blueprint for the poll API
poll_api = Blueprint('poll_api', __name__, url_prefix='/api/')
api = Api(poll_api)

db_path = 'instance/volumes/user_management.db'
CORS(poll_api)
# Create a class for the poll API
class Poll:
    class _Read(Resource):
        def get(self):
            try:
                # Retrieve the poll data
                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()
                query = 'SELECT _name, _interests FROM users;'  # Query to get the interests and names of users
                cursor.execute(query)
                results = cursor.fetchall()
                connection.close()

                # Convert the results to JSON
                response_data = [{"name": row[0], "interests": row[1]} for row in results]

                return response_data, 200
            except Exception as e:
                print(f"Poll Error: {e}")
                return {'message': 'Error retrieving poll data'}, 400
        
    api.add_resource(_Read, '/poll_read')
    
    class _Write(User, Resource):
        def post(self):
            try:
                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()
                
                # insert code to add to db here:
                
            except Exception as e:
                print(f"Poll Error: {e}")