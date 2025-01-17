from __init__ import db

class Poll(db.Model):
    __tablename__ = 'polls'

    # Match the existing columns in the DB
    pid       = db.Column('_pid', db.Integer, primary_key=True)
    name      = db.Column('_name', db.String(100), nullable=False)
    interests = db.Column('_interests', db.String(500), nullable=True)

    def __init__(self, name, interests):
        self.name = name
        self.interests = interests

    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "interests": self.interests
        }
