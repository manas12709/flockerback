from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from model.user import User

class TopInterest(db.Model):
    """
    TopInterest Model

    Represents an interest and the number of users who share it.
    """
    __tablename__ = 'top_interests'

    rank = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String(50), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, interest, count):
        """
        Constructor to initialize a TopInterest.

        Args:
            interest (str): The name of the interest.
            count (int): The number of users who share this interest.
        """
        self.interest = interest
        self.count = count

    def create(self):
        """
        Add the interest to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the interest's data as a dictionary.

        Returns:
            dict: Dictionary with interest information.
        """
        return {
            "rank": self.rank,
            "interest": self.interest,
            "count": self.count
        }

    def update(self, interest, count):
        """
        Update the interest and count, then commit the transaction.

        Args:
            interest (str): The name of the interest.
            count (int): The number of users who share this interest.
        """
        try:
            self.interest = interest
            self.count = count
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Remove the interest from the database and commit the transaction.
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
        Restore interests from a list of dictionaries.

        Args:
            data (list): List of dictionaries containing interest data.

        Returns:
            dict: Dictionary of restored TopInterest objects.
        """
        restored_interests = {}
        for interest_data in data:
            interest = interest_data.get("interest")
            count = interest_data.get("count")
            if not interest or count is None:
                raise ValueError("Missing required fields: interest or count.")

            top_interest = TopInterest.query.filter_by(interest=interest).first()
            if top_interest:
                top_interest.update(interest, count)
            else:
                top_interest = TopInterest(interest=interest, count=count)
                top_interest.create()

            restored_interests[interest] = top_interest

        return restored_interests


def initTopInterests():
    """
    Initialize the TopInterest table with default data.
    """
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Static data
        top_interests = [
            Interest("Music", "150"),
            Interest("Technology", "120"),
            Interest("Physics", "100"),
            Interest("Chemistry", "80"),
            Interest("Sports", "60"),
            Interest("Art", "40")
        ]

        # Add static data to the database
        for rank, interest_data in enumerate(static_interests, start=1):
            try:
                interest = TopInterest(**interest_data)
                interest.rank = rank
                db.session.add(interest)
                db.session.commit()
                print(f"Added Static Interest: Rank {rank}, {interest.interest}, Count {interest.count}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: Rank {rank}, {interest_data['interest']}")

        # Retrieve all users
        users = User.query.all()

        # Count the occurrences of each interest
        interest_counts = {}
        for user in users:
            interests = user.interests.split(", ")
            for interest in interests:
                if interest in interest_counts:
                    interest_counts[interest] += 1
                else:
                    interest_counts[interest] = 1

        # Sort interests by count in descending order
        sorted_interests = sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)

        # Create TopInterest entries from user data
        for rank, (interest, count) in enumerate(sorted_interests, start=1):
            try:
                top_interest = TopInterest(interest=interest, count=count)
                top_interest.rank = rank
                db.session.add(top_interest)
                db.session.commit()
                print(f"Added User Interest: Rank {rank}, {interest}, Count {count}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: Rank {rank}, {interest}")