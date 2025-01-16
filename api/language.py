from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.language import Language

# Define the Blueprint for the Language API
language_api = Blueprint('language_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(language_api)

class LanguageAPI:
    """
    Define the API CRUD endpoints for the Language model.
    """

    class _CRUD(Resource):
        def post(self):
            """
            Create a new language.
            """
            data = request.get_json()

            # Validate required fields
            if not data or 'name' not in data or 'paradigm' not in data:
                return {'message': 'Name and paradigm are required'}, 400

            # Create a new Language object
            language = Language(
                name=data['name'],
                paradigm=data['paradigm'],
                designed_by=data.get('designed_by', ''),
                first_appeared=data.get('first_appeared', ''),
                typing_discipline=data.get('typing_discipline', '')
            )

            # Save the language using the ORM method
            try:
                language.create()
                return jsonify(language.read())
            except Exception as e:
                return {'message': f'Error creating language: {e}'}, 500

        def get(self):
            """
            Retrieve all languages or a specific language by ID.
            """
            language_id = request.args.get('id')

            if language_id:
                # Get a specific language by ID
                language = Language.query.get(language_id)
                if not language:
                    return {'message': 'Language not found'}, 404
                return jsonify(language.read())

            # Get all languages
            languages = Language.query.all()
            return jsonify([language.read() for language in languages])

        def put(self):
            """
            Update an existing language by ID.
            """
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a language'}, 400

            # Find the language by ID
            language = Language.query.get(data['id'])
            if not language:
                return {'message': 'Language not found'}, 404

            # Update the language
            try:
                for key, value in data.items():
                    if hasattr(language, key):
                        setattr(language, key, value)
                db.session.commit()
                return jsonify(language.read())
            except Exception as e:
                return {'message': f'Error updating language: {e}'}, 500

        def delete(self):
            """
            Delete a language by ID.
            """
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a language'}, 400

            # Find the language by ID
            language = Language.query.get(data['id'])
            if not language:
                return {'message': 'Language not found'}, 404

            # Delete the language
            try:
                language.delete()
                return {'message': 'Language deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting language: {e}'}, 500

    class _BY_PARADIGM(Resource):
        def get(self):
            """
            Retrieve all languages from a specific paradigm.
            """
            paradigm = request.args.get('paradigm')

            if not paradigm:
                return {'message': 'Paradigm is required'}, 400

            languages = Language.query.filter(Language.paradigm.like(f"%{paradigm}%")).all()
            if not languages:
                return {'message': 'No languages found for the specified paradigm'}, 404

            return jsonify([language.read() for language in languages])

    # Map the resources to API endpoints
    api.add_resource(_CRUD, '/language')
    api.add_resource(_BY_PARADIGM, '/language/paradigm')
