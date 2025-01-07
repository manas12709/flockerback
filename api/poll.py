from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json
import sqlite3
#original code, not copied from templates/mr. mort

# Create blueprint for the poll API
poll_api = Blueprint('poll_api', __name__, url_prefix='/api/')
api = Api(poll_api)

db_path = 

# Create a class for the poll API
class Poll:
    
    class _Read(Resource):
        try:
            #retrieve the poll data
            connection = sqlite3.connect('instance/volumes/user_management.db')
            cursor = connection.cursor()
            query = 'SELECT _name,_interests FROM users;'
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            
            return results