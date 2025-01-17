from __init__ import db

class Language(db.Model):
    """
    Language Model

    This model represents a programming language, including its name, creator, release date, and current version.
    """
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    creator = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    current_version = db.Column(db.String(20), nullable=False)
    paradigm = db.Column(db.String(100), nullable=False)  # Programming paradigm(s)

    def __init__(self, name, creator, release_date, current_version, paradigm):
        self.name = name
        self.creator = creator
        self.release_date = release_date
        self.current_version = current_version
        self.paradigm = paradigm

    def create(self):
        """
        Add the language to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the language's data as a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "creator": self.creator,
            "release_date": self.release_date,
            "current_version": self.current_version,
            "paradigm": self.paradigm
        }

    def delete(self):
        """
        Remove the language from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initLanguages():
    """
    Initialize the Language table with default data.
    """
    languages = [
        Language("Python", "Guido van Rossum", "February 20, 1991", "3.10.0", "Object-oriented, Imperative, Functional, Procedural, Reflective"),
        Language("JavaScript", "Brendan Eich", "December 4, 1995", "ECMAScript 2021", "Event-driven, Functional, Imperative"),
        Language("Java", "James Gosling", "May 23, 1995", "16", "Object-oriented, Class-based, Concurrent"),
        Language("C++", "Bjarne Stroustrup", "October 1985", "C++20", "Object-oriented, Generic, Functional, Procedural"),
        Language("Ruby", "Yukihiro Matsumoto", "December 21, 1995", "3.0.2", "Object-oriented, Reflective, Imperative, Functional"),
        Language("Go", "Robert Griesemer, Rob Pike, Ken Thompson", "March 10, 2012", "1.17", "Compiled, Concurrent, Imperative, Structured")
    ]

    for language in languages:
        try:
            db.session.add(language)
            db.session.commit()
            print(f"Added Language: {language.name}")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding {language.name}: {e}")

@staticmethod
def restore(data):
    """
    Restore languages from a list of dictionaries.
    """
    restored_languages = {}
    for language_data in data:
        try:
            _ = language_data.pop('id', None)  # Remove 'id' from language_data
            name = language_data.get("name")
            creator = language_data.get("creator")

            if not name or not creator:
                raise ValueError("Missing required fields: name or creator.")

            # Generate a unique key using the language's name
            language_key = name

            # Check if a language with the same name exists
            language = Language.query.filter_by(name=name).first()

            if language:
                # Update the existing language's data
                language.update(language_data)
            else:
                # Create a new language if not found
                language = Language(**language_data)
                language.create()

            # Add the language to the restored_languages dictionary
            restored_languages[language_key] = language

        except Exception as e:
            print(f"Error processing language data: {language_data} - {e}")
            continue

    return restored_languages
