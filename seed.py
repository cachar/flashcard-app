"""Utility file to seed politician info database from Sunlight Foundation API"""



from model import connect_to_db, db
from server import app, HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE
from service import SunlightClient, PoliticianImporter, ExecutivePresenter











def load_politicians():
    """Load politicians from Sunlight Foundation API."""

    # Get federal congressional representatives.
    client = SunlightClient()
    PoliticianImporter(client.fetch_congress).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)
    PoliticianImporter(client.fetch_state_ppl).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)
    PoliticianImporter(ExecutivePresenter.fetch).add_or_update(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE)


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_politicians()




