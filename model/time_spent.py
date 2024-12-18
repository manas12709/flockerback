from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class TimeSpent(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    time_spent = Column(Integer, nullable=False)  # Time in seconds

    user = relationship("User", backref="time_spent")

    def __repr__(self):
        return f"<TimeSpent user_id={self.user_id}, time_spent={self.time_spent}>"
