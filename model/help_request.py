from __init__ import app, db

class HelpRequest(db.Model):
    """
    HelpRequest Model
    
    The HelpRequest class represents a help request submitted by a user.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the record.
        message (db.Column): A string representing the help request message.
        response (db.Column): A string representing the response to the help request.
        status (db.Column): A string representing the status of the help request.
        user_id (db.Column): An integer representing the ID of the user who submitted the help request.
    """
    __tablename__ = 'help_requests'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    response = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, user_id, response=None, status='Pending'):
        """
        Constructor, initializes a HelpRequest object.
        
        Args:
            message (str): The help request message.
            user_id (int): The ID of the user who submitted the help request.
            response (str): The response to the help request (default is None).
            status (str): The status of the help request (default is 'Pending').
        """
        self.message = message
        self.user_id = user_id
        self.response = response
        self.status = status

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"HelpRequest(id={self.id}, message={self.message}, response={self.response}, status={self.status}, user_id={self.user_id})"
    
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
        Deletes the help request from the database.
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
            dict: A dictionary containing the help request data.
        """
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'status': self.status,
            'user_id': self.user_id
        }

    def update(self, data):
        """
        Updates the help request with the provided data.
        
        Args:
            data (dict): A dictionary containing the updated data.
        
        Returns:
            HelpRequest: The updated help request object.
        """
        try:
            for key, value in data.items():
                setattr(self, key, value)
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e

def initHelpRequests():
    """
    The initHelpRequests function creates the HelpRequests table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        HelpRequest objects with tester data.
    
    Raises:
        Exception: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        tester_data = [
            HelpRequest(message='Need help with login', user_id=1),
            HelpRequest(message='Unable to access dashboard', user_id=2),
            HelpRequest(message='Error in report generation', user_id=3)
        ]
        
        for data in tester_data:
            try:
                db.session.add(data)
                db.session.commit()
                print(f"Record created: {repr(data)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating record for help request {data.message}: {e}")