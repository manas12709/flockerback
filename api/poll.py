from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json

# Create blueprint for the poll API
poll_api = Blueprint('poll_api', __name__, url_prefix='/api/')
api = Api(poll_api)

