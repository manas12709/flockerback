from __init__ import app, db

class Language(db.Model):
    """
    Language Model
    
    The Language class represents a programming language.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the record.
        name (db.Column): A string representing the name of the programming language.
        creator (db.Column): A string representing the creator of the programming language.
    """
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    creator = db.Column(db.String(255), nullable=False)

    def __init__(self, name, creator):
        """
        Constructor, initializes a Language object.
        
        Args:
            name (str): The name of the programming language.
            creator (str): The creator of the programming language.
        """
        self.name = name
        self.creator = creator

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Language(id={self.id}, name={self.name}, creator={self.creator})"
    
    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Deletes the language from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the language data.
        """
        return {
            'id': self.id,
            'name': self.name,
            'creator': self.creator
        }

def initLanguages():
    """
    The initLanguages function creates the Languages table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Language objects with tester data.
    
    Raises:
        Exception: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        tester_data = [
            Language(name='Python', creator='Guido van Rossum'),
            Language(name='JavaScript', creator='Brendan Eich'),
            Language(name='Java', creator='James Gosling')
        ]
        
        for data in tester_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for language {data.name}: {e}")