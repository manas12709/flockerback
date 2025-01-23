import logging
from sqlite3 import IntegrityError
from sqlalchemy import Text
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.user import User
from model.channel import Channel

class Chat(db.Model):
    """
    Chat Model
    
    The Chat class represents individual messages in a chat channel.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the chat message.
        _message (db.Column): A string representing the content of the message.
        _user_id (db.Column): An integer representing the user who sent the message.
        _channel_id (db.Column): An integer representing the channel to which the message belongs.
    """
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    _message = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    def __init__(self, message, user_id, channel_id):
        """
        Constructor for Chat Model.
        
        Args:
            message (str): The content of the chat message.
            user_id (int): The ID of the user sending the message.
            channel_id (int): The ID of the channel where the message is sent.
        """
        self._message = message
        self._user_id = user_id
        self._channel_id = channel_id

    def __repr__(self):
        return f"Chat(id={self.id}, message={self._message}, user_id={self._user_id}, channel_id={self._channel_id})"

    def create(self):
        """
        Saves the chat message to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not create chat message due to {str(e)}.")
            return None
        return self

    def read(self):
        """
        Retrieves chat message data as a dictionary.
        """
        user = User.query.get(self._user_id)
        channel = Channel.query.get(self._channel_id)
        return {
            "id": self.id,
            "message": self._message,
            "user_name": user.name if user else None,
            "channel_name": channel.name if channel else None,
        }

    def delete(self):
        """
        Deletes the chat message from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initChats():
    """
    The initChats function creates the Chat table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Chat objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        chats = [
            Chat(message="Hello, everyone!", user_id=1, channel_id=1),
            Chat(message="How's it going?", user_id=2, channel_id=1),
            Chat(message="Welcome to channel 2!", user_id=3, channel_id=2),
            Chat(message="Let's discuss project updates.", user_id=1, channel_id=2),
            Chat(message="Testing the chat system.", user_id=4, channel_id=1),
            Chat(message="This channel is for general discussions.", user_id=2, channel_id=3),
            Chat(message="Excited to collaborate with you all!", user_id=3, channel_id=1),
        ]
        
        for chat in chats:
            try:
                chat.create()
                print(f"Record created: {repr(chat)}")
            except IntegrityError:
                '''Fails with bad or duplicate data'''
                db.session.remove()
                print(f"Record exists or error: {chat.message}")
