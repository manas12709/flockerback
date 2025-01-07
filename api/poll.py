from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json
import sqlite3
#original code, not copied from templates/mr. mort/ChatGPT

# Create blueprint for the poll API
poll_api = Blueprint('poll_api', __name__, url_prefix='/api/')
api = Api(poll_api)

db_path = 'instance/volumes/user_management.db'

# Create a class for the poll API
class Poll:
    
    class _Read(Resource):
        def get(self):
            try:
                #retrieve the poll data
                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()
                query = 'SELECT _name,_interests FROM users;' # query to get the interests and names of users
                cursor.execute(query)
                results = cursor.fetchall()
                connection.close()
                
                return results, 200
            except:
                return {'message': 'Error retrieving poll data'}, 400
        
    api.add_resource(_Read, '/poll_read')