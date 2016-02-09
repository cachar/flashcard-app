"""Utility file to seed politician info database from Sunlight Foundation API"""

from sqlalchemy import func
from model import Politician

from model import connect_to_db, db
from server import app

import requests
#import sunlight
#from server import app
#import datetime
#sunlight.config.API_KEY = "19a86558186a4bf8857e67e56f6c9f88"
SUNLIGHT_API_KEY = "19a86558186a4bf8857e67e56f6c9f88"
HACKBRIGHT_LATITUDE = "37.788666"
HACKBRIGHT_LONGITUDE = "-122.411462"

#class sunlight.services.congress.Congress(use_https=True)
#    Congress.locate_legislators_by_lat_lon(HACKBRIGHT_LATITUDE, HACKBRIGHT_LONGITUDE, **kwargs)
#    pass


def get_congress_legislators(HACKBRIGHT_LATITUDE=HACKBRIGHT_LATITUDE,
                             HACKBRIGHT_LONGITUDE=HACKBRIGHT_LONGITUDE,
                             SUNLIGHT_API_KEY=SUNLIGHT_API_KEY):
    payload = {"server": "nginx/1.1.19",
               "date": "Tue, 09 Feb 2016 00:26:43 GMT",
               "content-type": "application/json; charset=utf-8",
               "content-length": "2712",
               "connection": "keep-alive",
               "vary": "Accept-Encoding",
               "status": "200 OK"}

    url = "http://congress.api.sunlightfoundation.com/legislators/locate?latitude=%s&longitude=%s&apikey=%s" % (HACKBRIGHT_LATITUDE,
                                                                                                                HACKBRIGHT_LONGITUDE,
                                                                                                                SUNLIGHT_API_KEY)

    r = requests.get(url, params=payload)
    jdict = r.json()

    for result in jdict["results"]:
        bioguide_id = result['bioguide_id']
        name = result['first_name'] + result['last_name']
        party = result['party']
        title = result['title']
        photo_url = 'https://theunitedstates.io/images/congress/225x275/' + pol_id + '.jpg'
        district = result['district']
        if district is None:
            district = result['state_name']

        politician = Politician(bioguide_id=bioguide_id,
                                name=name,
                                title=title,
                                district=district,
                                party_id=party,
                                photo_url=photo_url)

        db.session.add(politician)

    db.session.commit()

def load_politicians():
    """Load politicians from Sunlight Foundation API."""
    
    # Get federal congressional representatives.
    get_congress_legislators()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_politicians()




