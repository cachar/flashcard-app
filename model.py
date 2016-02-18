"""Models and database functions for Flashcard project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from random import shuffle

db = SQLAlchemy()

#Model definitions


class Politician(db.Model):
    """Politicians of flashcard database"""

    __tablename__ = "politicians"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    constituency = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(50), nullable=False)
    bioguide_id = db.Column(db.String(50), nullable=False, unique=True)
    photo_url = db.Column(db.String(150), nullable=False, unique=True)


    @classmethod
    def questionable_fields(cls):
        return ["name", "title", "constituency", "party"]

    def value(self, field):
        if field == "name":
            return self.name
        elif field == "title":
            return self.title
        elif field == "constituency":
            return self.constituency
        elif field == "party":
            return self.party


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
    scored = db.Column(db.Boolean, nullable=False)

    @validates('field')
    def validate_field(self, key, field):
        assert field in Politician.questionable_fields()
        return field

    def score(self):
        computed_score = 0
        for card in self.politician_cards:
            if card.correct():
                computed_score += 1

        return computed_score

    def card_count(self):
        return PoliticianCard.query.filter_by(card_deck_id=self.id).count()

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CardDeck id=%s field=%s>" % (self.id, self.field)


class PoliticianCard(db.Model):
    """Question with a politician and a field."""

    __tablename__ = "politician_cards"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'), nullable=False)
    card_deck_id = db.Column(db.Integer, db.ForeignKey('card_decks.id'), nullable=False)
    field = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.String(100), nullable=True)


    politician = db.relationship('Politician',
                                 backref="politician_cards")
    card_deck = db.relationship('CardDeck',
                                     backref="politician_cards")

    def right_answer(self):
        return self.politician.value(self.field)

    def wrong_answers(self):
        answers = [p.value(self.field) for p in Politician.query.all()]
        answers = list(set(answers))
        if answers == []:
            if self.field == "party":
                if right_answer == "D":
                    answers = ["R"]
                else:
                    answers = ["D"]
        return answers

    def possible_answers(self):
        right_answer = self.right_answer()
        wrong_answers = self.wrong_answers()
        wrong_answers.remove(right_answer)
        shuffle(wrong_answers)
        all_answers = [right_answer] + wrong_answers[0:3]
        shuffle(all_answers)
        return all_answers

    def correct(self):
        return self.answer == self.right_answer()

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<PoliticianCard id=%s politician_id=%s field=%s>" % (self.id,
                                                                         self.politician_id,
                                                                         self.card_deck.field)





def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flashcards'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print "Connected to DB"
    print PoliticianCard.query.get(1).possible_answers()
