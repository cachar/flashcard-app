"""Models and database functions for Flashcard project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from random import shuffle
from datetime import datetime

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
    """Collection of politician cards."""

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
    """Card with a politician and a field."""

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

        if self.field == "party" and len(answers) == 1:
            if self.right_answer() == "D":
                answers += ["R"]
            elif self.right_answer() == "R":
                answers += ["D"]
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


class HighScore(db.Model):
    """Collection of card deck scores."""

    ___tablename___ = "high_scores"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    @classmethod
    def top_five_scores(cls):
        return cls.query.order_by(HighScore.score.desc()).limit(5).all()

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<HighScore id=%s score=%s timestamp=%s" % (self.id,
                                                           self.score,
                                                           self.timestamp)


##############################################################

def example_data_high_scores():
    """Create some fake politicians for test db"""

    # Delete existing data in case test is run more than once
    HighScore.query.delete()

    # Add new fake data
    for i in range(6):
        new_high_score = HighScore(score=i*10.1,
                                   timestamp=datetime.now(),
                                   name="Balloonicorn")
        db.session.add(new_high_score)

    db.session.commit()


def connect_to_db(app, database):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = database
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app, 'postgresql:///flashcards')
    print "Connected to DB"

