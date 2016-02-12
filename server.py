from flask import Flask, render_template, redirect, request
from model import *
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def landing_page():
    return render_template("homepage.html")

@app.route('/card_decks', methods=["GET"])
def show_card_decks():
    fields = Politician.questionable_fields()
    card_decks = CardDeck.query.all()
    return render_template("card_decks.html", card_decks=card_decks, fields=fields)

@app.route('/card_decks/new', methods=["GET"])
def new_card_deck():
    fields = Politician.questionable_fields()
    return render_template("new_card_deck.html", fields=fields)

@app.route('/card_decks', methods=["POST"])
def create_card_deck():
    field = request.form.get("field")
    card_deck = CardDeck(field=field)

    politicians = Politician.query.all()

    for politician in politicians:
        card = PoliticianCard(card_deck=card_deck, politician=politician, field=field)

        db.session.add(card)

    db.session.add(card_deck)
    db.session.commit()

    return redirect('/card_decks/%s' % card_deck.id)

@app.route('/card_decks/<int:id>', methods=["GET"])
def show_card_deck(id):

    card = PoliticianCard.query.filter_by(card_deck_id=id, answer=None).first()
    if card == None:

        return redirect("/card_decks/%s/score" % id)
    else:
        return redirect('/cards/%s' % card.id)

@app.route('/card_decks/<int:id>/score', methods=["GET"])
def show_score(id):

    card_deck = CardDeck.query.get(id)
    return render_template("score.html", card_deck=card_deck)



@app.route('/card_decks/<int:id>/cards', methods=["GET"])
def show_card_deck_cards(id):

    card_deck = CardDeck.query.get(id)
    # import pdb
    # pdb.set_trace()
    return render_template("card_deck_details.html", card_deck=card_deck, field=card_deck.field)

@app.route('/cards/<int:id>', methods=["GET"])
def show_card(id):

    card = PoliticianCard.query.get(id)

    return render_template("card_details.html", card=card)

@app.route('/cards/<int:id>', methods=["POST"])
def create_card_answer(id):

    card = PoliticianCard.query.get(id)
    answer = request.form.get("answer")

    card.answer = answer
    db.session.commit()

    return redirect('/card_decks/%s' % card.card_deck.id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
