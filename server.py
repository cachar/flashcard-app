from flask import Flask, render_template, redirect, request, flash
from model import *
from  sqlalchemy.sql.expression import func
from flask_debugtoolbar import DebugToolbarExtension
from random import shuffle
from datetime import datetime
from sqlalchemy import desc

from jinja2 import StrictUndefined

from service import SunlightClient, PoliticianImporter, ExecutivePresenter

app = Flask(__name__)


HACKBRIGHT_LATITUDE = "37.788666"
HACKBRIGHT_LONGITUDE = "-122.411462"

client = SunlightClient()
congress_importer = PoliticianImporter(client.fetch_congress)
state_importer = PoliticianImporter(client.fetch_state_ppl)
executive_importer = PoliticianImporter(ExecutivePresenter.fetch)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def landing_page():
    """Show landing page."""

    return render_template("homepage.html",
                           latitude=HACKBRIGHT_LATITUDE,
                           longitude=HACKBRIGHT_LONGITUDE)


@app.route('/flashcards/new', methods=["GET"])
def new_flashcards():
    """Show user a menu of possible fields to review in flashcard format."""

    fields = Politician.questionable_fields()
    return render_template("new_card_deck.html",
                           fields=fields,
                           scored=False,
                           latitude=HACKBRIGHT_LATITUDE,
                           longitude=HACKBRIGHT_LONGITUDE)

@app.route('/quizzes/new', methods=["GET"])
def new_quiz():
    """Show user a menu of possible fields to get quizzed over."""

    fields = Politician.questionable_fields()
    return render_template("new_card_deck.html",
                           fields=fields,
                           scored=True,
                           latitude=HACKBRIGHT_LATITUDE,
                           longitude=HACKBRIGHT_LONGITUDE)

@app.route('/card_decks', methods=["POST"])
def create_card_deck():
    """Call Sunlight API, make a deck of politician flashcards. Redirect to first card of the new deck."""

    field = request.form.get("field")
    scored = request.form.get("scored") == "True"
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    card_deck = CardDeck(field=field, scored=scored)

    politicians = load_politicians(latitude, longitude)


    shuffle(politicians)
    for politician in politicians:
        card = PoliticianCard(card_deck=card_deck, politician=politician, field=field)

        db.session.add(card)

    db.session.add(card_deck)
    db.session.commit()

    return redirect('/card_decks/%s' % card_deck.id)

@app.route('/card_decks/<int:id>', methods=["GET"])
def show_card_deck(id):
    """Redirect to a card for a politician, until deck is exhausted. Show a score at
    the end if in quiz mode."""

    card_deck = CardDeck.query.get(id)
    card = PoliticianCard.query.filter_by(card_deck_id=id, answer=None).first()
    if card == None:
        if card_deck.scored:
            return redirect("/card_decks/%s/score" % id)
        else:
            flash("End of flashcards!")
            return redirect('/')
    else:
        return redirect('/cards/%s' % card.id)



@app.route('/cards/<int:id>', methods=["GET"])
def show_card(id):
    """Show a card."""

    card = PoliticianCard.query.get(id)
    if card.card_deck.scored:
        return render_template("quiz.html", card=card)
    else:
        return render_template("flashcard.html", card=card)


@app.route('/cards/<int:id>', methods=["POST"])
def create_card_answer(id):
    """Show a card for quiz mode, posting the answer from the previous card."""

    card = PoliticianCard.query.get(id)
    answer = request.form.get("answer")

    card.answer = answer
    db.session.commit()

    return redirect('/card_decks/%s' % card.card_deck.id)



@app.route('/card_decks/<int:id>/score', methods=["GET"])
def show_score(id):
    """Show score for end of quiz mode."""

    card_deck = CardDeck.query.get(id)
    score = card_deck.score()
    card_count = card_deck.card_count()
    score_grade = float(score) / card_count * 100
    score_grade = float("{0:.2f}".format(score_grade))

    is_new_high_score = False

    top_five_score_objects = HighScore.top_five_scores()

    for score_object in top_five_score_objects:
        if score_grade > score_object.score:

            flash("New high score!")
            is_new_high_score = True


            break

    return render_template("score.html",
                           card_deck=card_deck,
                           is_new_high_score=is_new_high_score,
                           score_grade=score_grade)



@app.route('/notes', methods=["GET"])
def show_notes():
    """Query API for politicians, then show in notes form. Query local
    database if API is down."""



    politicians = Politician.query.all()


    return render_template("notes.html", politicians=politicians)

@app.route('/high_scores', methods=["GET"])
def show_high_scores():
    """Display top 5 high scores"""

    user = request.args.get("user")
    score_grade = request.args.get("score_grade")
    if user != "":
        high_score = HighScore(score=score_grade,
                           timestamp=datetime.now(),
                           name=user)
        db.session.add(high_score)
        db.session.commit()

    high_scores = HighScore.top_five_scores()

    return render_template("high_scores.html", high_scores=high_scores)


def load_politicians(latitude, longitude):
    """Try to fetch from API, otherwise query from local database."""

    try:
        congressional_politicians = congress_importer.add_or_update(latitude, longitude)
        state_politicians = state_importer.add_or_update(latitude, longitude)
        executive_politicians = executive_importer.add_or_update(latitude, longitude)

        politicians = congressional_politicians + state_politicians + executive_politicians

    except ValueError:
        politicians = Politician.query.all()

    return politicians



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app, 'postgresql:///flashcards')

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
