"""Models and database functions for Flashcard project."""

from flask_sqlalchemy import SQLAlchemy

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
    district = db.Column(db.String(100), nullable=False)
    party_name = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(140), nullable=False)
    bioguide_id = db.Column(db.String(50), nullable=False, unique=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Politician politician_id=%s name=%s title=%s>" % (self.id,
                                                                   self.name,
                                                                   self.title)

class QuestionSet(db.Model):
    """Set of questions."""

    __tablename__ = "question_sets"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<QuestionSet id=%s field=%s>" % (self.id, self.field)


class Question(db.Model):
    """Question with a politician and a field."""

    __tablename__ = "questions"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'), nullable=False)
    question_set_id = db.Column(db.Integer, db.ForeignKey('question_sets.id'), nullable=False)

    politician = db.relationship('Politician',
                                 backref="questions")
    question_set = db.relationship('QuestionSet',
                                     backref="questions")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question id=%s politician_id=%s question_set_id=%s>" % (self.id,
                                                                         self.politician_id,
                                                                         self.question_set_id)





def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flashcards'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print "Connected to DB"

