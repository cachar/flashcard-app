from flask import Flask, render_template, redirect
from model import *
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def landing_page():
    return render_template("about.html")

@app.route('/card_decks', methods=["GET"])
def show_card_decks():

    card_decks = CardDeck.query.all()
    return render_template("card_decks.html", card_decks=card_decks)

@app.route('/card_decks', methods=["POST"])
def create_card_deck():
    
    card_deck= CardDeck(field=Politician.questionable_field())
    politician = Politician.query.get(1)
    card = PoliticianCard(card_deck=card_deck, politician=politician)
    #make many politician_cards
    db.session.add(card)

    db.session.add(card_deck)
    db.session.commit()

    return redirect('/card_decks')

@app.route('/card_decks/<int:id>')
def show_card_deck(id):

    card_deck = CardDeck.query.get(id)

    return render_template("card_deck_details.html", card_deck=card_deck)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()