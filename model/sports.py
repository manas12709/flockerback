from __init__ import db

class Player(db.Model):
    """
    Player Model

    This model represents a sports player, including their personal details, team affiliation, and the sports they play.
    """
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    residence = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    team = db.Column(db.String(100), nullable=False)  # Name of the team the player belongs to
    sports_played = db.Column(db.String(500), nullable=True)  # Comma-separated list of sports

    def __init__(self, first_name, last_name, dob, residence, email, team, sports_played):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.residence = residence
        self.email = email
        self.team = team
        self.sports_played = ', '.join(sports_played) if isinstance(sports_played, list) else sports_played

    def create(self):
        """
        Add the player to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the player's data as a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob,
            "residence": self.residence,
            "email": self.email,
            "team": self.team,
            "sports_played": self.sports_played.split(', ') if self.sports_played else []
        }

    def delete(self):
        """
        Remove the player from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initPlayers():
    """
    Initialize the Player table with default data.
    """
    players = [
        Player("LeBron", "James", "December 30", "Los Angeles", "lebron@nba.com", "Los Angeles Lakers", ["Basketball"]),
        Player("Lionel", "Messi", "June 24", "Miami", "messi@mls.com", "Inter Miami CF", ["Soccer"]),
        Player("Serena", "Williams", "September 26", "Florida", "serena@wta.com", "Retired", ["Tennis"]),
        Player("Tom", "Brady", "August 3", "Tampa", "tom@tb12.com", "Retired", ["Football"]),
        Player("Usain", "Bolt", "August 21", "Kingston", "usain@track.com", "Retired", ["Track and Field"]),
        Player("Simone", "Biles", "March 14", "Houston", "simone@gymnastics.com", "USA Gymnastics", ["Gymnastics"]),
    ]

    for player in players:
        try:
            db.session.add(player)
            db.session.commit()
            print(f"Added Player: {player.first_name} {player.last_name}")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding {player.first_name} {player.last_name}: {e}")
