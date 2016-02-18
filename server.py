from flask import Flask, render_template, redirect, request, flash
from model import *
from  sqlalchemy.sql.expression import func
from flask_debugtoolbar import DebugToolbarExtension
from random import shuffle

from jinja2 import StrictUndefined

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def landing_page():
    return render_template("homepage.html")


@app.route('/flashcards/new', methods=["GET"])
def new_flashcards():
    fields = Politician.questionable_fields()
    return render_template("new_card_deck.html", fields=fields, scored=False)

@app.route('/quizzes/new', methods=["GET"])
def new_quiz():
    fields = Politician.questionable_fields()
    return render_template("new_card_deck.html", fields=fields, scored=True)

@app.route('/card_decks', methods=["POST"])
def create_card_deck():
    field = request.form.get("field")
    scored = request.form.get("scored") == "True"
    card_deck = CardDeck(field=field, scored=scored)

    politicians = Politician.query.all()
    shuffle(politicians)
    for politician in politicians:
        card = PoliticianCard(card_deck=card_deck, politician=politician, field=field)

        db.session.add(card)

    db.session.add(card_deck)
    db.session.commit()

    return redirect('/card_decks/%s' % card_deck.id)

@app.route('/card_decks/<int:id>', methods=["GET"])
def show_card_deck(id):
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

    card = PoliticianCard.query.get(id)
    if card.card_deck.scored:
        return render_template("quiz.html", card=card)
    else:
        return render_template("flashcard.html", card=card)


@app.route('/cards/<int:id>', methods=["POST"])
def create_card_answer(id):

    card = PoliticianCard.query.get(id)
    answer = request.form.get("answer")

    card.answer = answer
    db.session.commit()

    return redirect('/card_decks/%s' % card.card_deck.id)



@app.route('/card_decks/<int:id>/score', methods=["GET"])
def show_score(id):

    card_deck = CardDeck.query.get(id)
    return render_template("score.html", card_deck=card_deck)



@app.route('/notes', methods=["GET"])
def show_notes():
    politicians = Politician.query.all()
    return render_template("notes.html", politicians=politicians)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
