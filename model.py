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

    ___tablename___ = "politicians"

    pol_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    party_id = db.Column(db.String(3), db.ForeignKey('parties.party_id'), nullable=False)
    photo_url = db.Column(db.String(140), nullable=False)

    party = db.relationship('Party',
                            backref="politicians")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Politician politician_id=%s name=%s title=%s>" % (self.pol_id,
                                                                   self.name,
                                                                   self.title)


class Party(db.Model):
    """Parties of flashcard database"""

    ___tablename___ = "parties"

    party_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    party_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Party party_id=%s party_name=%s>" % (self.party_id,
                                                      self.party_name)


class Flashcard(db.Model):
    """Flashcard with a politician and a field."""

    flashcard_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pol_id = db.Column(db.Integer, db.ForeignKey('politicians.pol_id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.type_id'), nullable=False)

    politician = db.relationship('Politician',
                                 backref="flashcards")
    flashcard_type = db.relationship('Type',
                                     backref="flashcards")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Flashcard flashcard_id=%s pol_id=%s flashcard_type=%s>" % (self.flashcard_id,
                                                                                   self.pol_id,
                                                                                   self.type_id)


class Type(db.Model):
    """Type of personal info."""

    type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Type type_id=%s field=%s>" % (self.type_id, self.field)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flashcards'
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

    from server import app
    connect_to_db(app)
    print "Connected to DB"

