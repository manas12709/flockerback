from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from model.user import User

class TopUser(db.Model):
    """
    TopUser Model

    The TopUser class represents a user with their interests and a score.
    """
    __tablename__ = 'top_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, name, interests, score):
        self.name = name
        self.interests = interests
        self.score = score

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "interests": self.interests,
            "score": self.score
        }

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def initTopUsers():
    with app.app_context():
        db.create_all()
        top_users = [
            TopUser(name='Alice', interests='reading, hiking', score=10),
            TopUser(name='Bob', interests='cooking, hiking', score=8),
        ]
        for top_user in top_users:
            top_user.create()