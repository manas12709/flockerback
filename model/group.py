from __init__ import app, db

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

    def __init__(self, name, section_id):
        self.name = name
        self.section_id = section_id

    def __repr__(self):
        return f"Group(id={self.id}, name={self.name}, section_id={self.section_id})"

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "section_id": self.section_id
        }

def initGroups():
    """
    The initGroups function creates the Group table and adds tester data to the table.
    """
    with app.app_context():
        db.create_all()
        # Example tester data
        groups = [
            Group(name='General', section_id=1),
            Group(name='Support', section_id=1),
            Group(name='Random Chatroom', section_id=2),
            Group(name='Daily Question', section_id=2),
            Group(name='Interests', section_id=2)
        ]
        for group in groups:
            try:
                db.session.add(group)
                db.session.commit()
                print(f"Record created: {repr(group)}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating group {group.name}: {e}")