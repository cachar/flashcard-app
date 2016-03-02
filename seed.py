"""Utility file to seed politician info database from Sunlight Foundation API"""



from model import connect_to_db, db, HighScore
from server import app, HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE
from service import SunlightClient, PoliticianImporter, ExecutivePresenter
from datetime import datetime

def load_politicians():
    """Load politicians from Sunlight Foundation API."""

    # Get federal congressional representatives.
    client = SunlightClient()
    PoliticianImporter(client.fetch_congress).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)
    PoliticianImporter(client.fetch_state_ppl).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)
    PoliticianImporter(ExecutivePresenter.fetch).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)

def initialize_high_scores():
    """Initialize 5 high scores."""

    for i in range(5):
        high_score = HighScore(score=0,
                               timestamp=datetime.now(),
                               name="Balloonicorn")
        db.session.add(high_score)
            
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_politicians()
    initialize_high_scores()




