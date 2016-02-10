"""Models and database functions for Flashcard project."""

from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

#Model definitions

# class Person(db.Model):
#     """People in the Star Trek TNG main cast."""

#     person_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     serial_number = db.Column(db.String(50), nullable=False, unique=True)
#     rank = db.Column(db.String(50))
#     actor = db.Column(db.String(50))
#     home
#     photo_url = pass


class Politician(db.Model):
    """Politicians of flashcard database"""

    __tablename__ = "politicians"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    constituency = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(50), nullable=False)
    bioguide_id = db.Column(db.String(50), nullable=False, unique=True)


    def photo_url(self):
        return 'https://theunitedstates.io/images/congress/225x275/' + self.bioguide_id + '.jpg'

    @classmethod
    def questionable_field(cls):
        return random.choice(["name", "title", "constituency", "party"])

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Politician politician_id=%s name=%s title=%s>" % (self.id,
                                                                   self.name,
                                                                   self.title)

class CardDeck(db.Model):
    """Set of questions."""

    __tablename__ = "card_decks"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CardDeck id=%s field=%s>" % (self.id, self.field)


class PoliticianCard(db.Model):
    """Question with a politician and a field."""

    __tablename__ = "politician_cards"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'), nullable=False)
    card_deck_id = db.Column(db.Integer, db.ForeignKey('card_decks.id'), nullable=False)

    politician = db.relationship('Politician',
                                 backref="politician_cards")
    card_deck = db.relationship('CardDeck',
                                     backref="politician_cards")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<PoliticianCard id=%s politician_id=%s card_deck_id=%s>" % (self.id,
                                                                         self.politician_id,
                                                                         self.card_deck_id)





def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flashcards'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print "Connected to DB"

