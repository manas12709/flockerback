from __init__ import app, db

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

    def __repr__(self):
        return f"Channel(id={self.id}, name={self.name}, group_id={self.group_id})"

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "group_id": self.group_id
        }

def initChannels():
    """
    The initChannels function creates the Channel table and adds tester data to the table.
    """
    with app.app_context():
        db.create_all()
        # Example tester data
        channels = [
            Channel(name='Announcements', group_id=1),
            Channel(name='Events', group_id=1),
            Channel(name='FAQ', group_id=2),
            Channel(name='Help Desk', group_id=2),
            Channel(name='Random Chatroom', group_id=3),
            Channel(name='Daily Question', group_id=4),
            Channel(name='Interests', group_id=5)
        ]
        for channel in channels:
            try:
                db.session.add(channel)
                db.session.commit()
                print(f"Record created: {repr(channel)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating channel {channel.name}: {e}")