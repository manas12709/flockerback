from __init__ import db

class SchoolClass(db.Model):
    """
    SchoolClass Model

    This model represents a school class with its subject and teacher information.
    """
    __tablename__ = 'school_classes'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(500), nullable=True)  # Comma-separated list of teachers

    def __init__(self, subject, teacher):
        self.subject = subject
        self.teacher = ', '.join(teacher) if isinstance(teacher, list) else teacher

    def create(self):
        """
        Add the school class to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the school class's data as a dictionary.
        """
        return {
            "id": self.id,
            "subject": self.subject,
            "teacher": self.teacher.split(', ') if self.teacher else []
        }

    def update(self, data):
        """
        Update the school class's data with the provided dictionary.
        """
        try:
            self.subject = data.get('subject', self.subject)
            teacher = data.get('teacher', self.teacher)
            self.teacher = ', '.join(teacher) if isinstance(teacher, list) else teacher
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Remove the school class from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initSchoolClasses():
    """
    Initialize the SchoolClass table with default data.
    """
    classes = [
        SchoolClass("Mathematics", ["Nydam", "Buehler", "Froom", "Larsen", "Hightower"]),
        SchoolClass("English", ["Hall", "Darcey", "Weeg"]),
        SchoolClass("Chemistry", ["Ozuna", "Callicott", "Millman"]),
        SchoolClass("Engineering", ["Mortensen", "Brown", "Campillo"]),
        SchoolClass("Physics", ["Liao", "Millman", "Eckman"])
    ]

    for school_class in classes:
        try:
            db.session.add(school_class)
            db.session.commit()
            print(f"Added School Class: {school_class.subject} taught by {school_class.teacher}")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding class {school_class.subject}: {e}")