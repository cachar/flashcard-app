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
        name = result['first_name'] + " " + result['last_name']
        party = result['party']
        title = result['title']
        constituency = result['district'] or result['state_name']
        photo_url = 'https://theunitedstates.io/images/congress/225x275/' + bioguide_id + '.jpg'

        politician = Politician.query.filter(Politician.bioguide_id == bioguide_id).first()

        if politician == None:
            politician = Politician(bioguide_id=bioguide_id,
                                    name=name,
                                    title=title,
                                    constituency=constituency,
                                    party=party,
                                    photo_url=photo_url)
            db.session.add(politician)
        else:
            politician.name = name
            politician.party = party
            politician.title = title
            politician.constituency = constituency

    db.session.commit()



def get_state_reps(HACKBRIGHT_LATITUDE=HACKBRIGHT_LATITUDE,
                   HACKBRIGHT_LONGITUDE=HACKBRIGHT_LONGITUDE,
                   SUNLIGHT_API_KEY=SUNLIGHT_API_KEY):
    
    payload = {"server": "nginx/1.4.1 (Ubuntu)",
               "content-type": "application/json; charset=utf-8",
               "vary": "Authorization",
               "access-control-allow-origin": "*",
               "content-length": "11097",
               "date": "Tue, 09 Feb 2016 00:35:05 GMT",
               "x-varnish": "1674567739",
               "age": "0",
               "via": "1.1 varnish",
               "connection": "keep-alive"}

    url = "http://openstates.org/api/v1//legislators/geo/?lat=%s&long=%s&apikey=%s" % (HACKBRIGHT_LATITUDE,
                                                                                       HACKBRIGHT_LONGITUDE,
                                                                                       SUNLIGHT_API_KEY)
    
    r = requests.get(url, params=payload)
    jdict = r.json()

    for result in jdict:
        name = result["full_name"]
        bioguide_id = result["leg_id"]
        party = result["party"]
        if party == "Democratic":
            party = "D"
        elif party == "Republican":
            party = "R"
        constituency = result["state"] + " " + result["district"]
        photo_url = result["photo_url"] 
        if name == "Mark Leno":
            photo_url = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Mark_Leno.jpg"

        if result["sources"] == [{"url": "http://assembly.ca.gov/assemblymembers"}]:
            title = "Assemblymember"
        elif result["sources"] == [{"url": "http://senate.ca.gov/senators"}]:
            title = "Senator"

        politician = Politician.query.filter(Politician.bioguide_id == bioguide_id).first()

        if politician == None:
            politician = Politician(bioguide_id=bioguide_id,
                                    name=name,
                                    title=title,
                                    constituency=constituency,
                                    party=party,
                                    photo_url=photo_url)
            db.session.add(politician)
        else:
            politician.name = name
            politician.party = party
            politician.title = title
            politician.constituency = constituency

    db.session.commit()

def hard_code_pres_and_vp():
    politician = Politician(bioguide_id="POTUS44",
                            name="Barack Obama",
                            title="President",
                            constituency="USA",
                            party="D",
                            photo_url="http://advocacyrelay.convio.net/images/advocacy/legislators/194235.jpg")
    db.session.add(politician)

    politician = Politician(bioguide_id="VPforP44",
                            name="Joe Biden",
                            title="Vice President",
                            constituency="USA",
                            party="D",
                            photo_url="http://advocacyrelay.convio.net/images/advocacy/legislators/165208.jpg")
    db.session.add(politician)

    db.session.commit()



def load_politicians():
    """Load politicians from Sunlight Foundation API."""
    
    # Get federal congressional representatives.
    get_congress_legislators()
    get_state_reps()
    hard_code_pres_and_vp()

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_politicians()




