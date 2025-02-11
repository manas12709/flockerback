from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from model.post import Post
from model.user import User

class Skibidi(db.Model):
    """
    Skibidi Model

    The Skibidi class represents a single upskibidi or downskibidi on a post by a user.

    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the skibidi.
        _skibidi_type (db.Column): A string representing the type of skibidi ("upskibidi" or "downskibidi").
        _user_id (db.Column): An integer representing the ID of the user who cast the skibidi.
        _post_id (db.Column): An integer representing the ID of the post that received the skibidi.
    """
    __tablename__ = 'testers'

    id = db.Column(db.Integer, primary_key=True)
    _skibidi_type = db.Column(db.String(10), nullable=False)  # "upskibidi" or "downskibidi"
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, skibidi_type, user_id, post_id):
        """
        Constructor to initialize a skibidi.

        Args:
            skibidi_type (str): Type of the skibidi, either "upskibidi" or "downskibidi".
            user_id (int): ID of the user who cast the skibidi.
            post_id (int): ID of the post that received the skibidi.
        """
        self._skibidi_type = skibidi_type
        self._user_id = user_id
        self._post_id = post_id

    def create(self):
        """
        Add the skibidi to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the skibidi data as a dictionary.

        Returns:
            dict: Dictionary with skibidi information.
        """
        return {
            "id": self.id,
            "skibidi_type": self._skibidi_type,
            "user_id": self._user_id,
            "post_id": self._post_id
        }
    
    def update(self, skibidi_type):
        """
        Update the skibidi type and commit the transaction.

        Args:
            skibidi_type (str): Type of the skibidi, either "upskibidi" or "downskibidi".
        """
        try:
            self._skibidi_type = skibidi_type
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def delete(self):
        """
        Remove the skibidi from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data):
        """
        Restore skibidis from a list of dictionaries.

        Args:
            data (list): List of dictionaries containing skibidi data.
        
        Returns:
            list: List of restored Skibidi objects.
        """
        restored_classes = {}
        for skibidi_data in data:
            skibidi = Skibidi(skibidi_data['skibidi_type'], skibidi_data['user_id'], skibidi_data['post_id'])
            skibidi.create()
            restored_classes[skibidi_data['id']] = skibidi
            
        return restored_classes


def initSkibidis():
    """
    Initialize the Skibidi table with any required starter data.
    """
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Optionally, add some test data (replace with actual values as needed)
        skibidis = [
            Skibidi(skibidi_type='upskibidi', user_id=1, post_id=5),
            Skibidi(skibidi_type='downskibidi', user_id=2, post_id=5),
            Skibidi(skibidi_type='upskibidi', user_id=2, post_id=1),
            Skibidi(skibidi_type='downskibidi', user_id=2, post_id=3),
        ]
        
        for skibidi in skibidis:
            try:
                db.session.add(skibidi)
                db.session.commit()
                print(f"Record created: {repr(skibidi)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: {repr(skibidi)}")
