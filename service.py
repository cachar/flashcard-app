
import requests
import os

from sqlalchemy import func
from model import Politician, db


class SunlightClient(object):
    """Create a class to handle fetching data from Sunlight Foundation APIs"""

    def __init__(self):
        self.key = os.environ['SUNLIGHT_API_KEY']

    def fetch_congress(self, latitude, longitude):
        """Fetch data from the Congress API, use CongressPresenter to turn
        JSON into a list of politician-like objects for easy adding/updating of
        database."""

        url = "http://congress.api.sunlightfoundation.com/legislators/locate"
        payload = {"latitude": latitude,
                    "longitude": longitude,
                    "apikey": self.key}

        r = requests.get(url, params=payload)
        results = r.json()['results']
        return [CongressPresenter(result) for result in results]

    def fetch_state_ppl(self, latitude, longitude):
        """Fetch data from the Open States API, use StatePresenter to turn
        JSON into a list of politician-like objects for easy adding/updating of
        database."""

        url = "http://openstates.org/api/v1//legislators/geo/"

        payload = {"lat": latitude,
                   "long": longitude,
                   "apikey": self.key}

        r = requests.get(url, params=payload)
        results = r.json()
        return [StatePresenter(result) for result in results]


class CongressPresenter(object):
    """Turn JSON from Congress API into a Politician-like object."""


    def __init__(self, result):
        self.result = result

    def bioguide_id(self):
        return self.result['bioguide_id']

    def name(self):
        return self.result['first_name'] + " " + self.result['last_name']

    def title(self):
        if self.result['title'] == "Sen":
            return "Senator"
        elif self.result['title'] == "Rep":
            return "Representative"
        else:
            return self.result['title']

    def constituency(self):
        if self.result['district'] == None:
            return self.result['state_name']
        else:
            return self.result['state_name'] + " district " + str(self.result['district'])

    def party(self):
        return self.result['party']

    def photo_url(self):
        return 'https://theunitedstates.io/images/congress/225x275/' + self.bioguide_id() + '.jpg'



class StatePresenter(object):
    """Turn JSON from Open States API into a Politician-like object."""


    def __init__(self, result):
        self.result = result

    def bioguide_id(self):
        return self.result['leg_id']

    def name(self):
        return self.result['full_name']

    def title(self):
        if self.result["chamber"] == "lower" and self.result["state"] == "ca":
            return "Assemblymember"
        elif self.result["chamber"] == "upper":
            return "Senator"
        else:
            return "Representative"

    def constituency(self):
        return self.result["state"].upper() + " state district " + self.result["district"]

    def party(self):
        return self.result['party'][0]

    def photo_url(self):
        photo_url = self.result['photo_url']

        return photo_url



class ExecutivePresenter(object):
    """Hard code in president and vice president as Politician-like objects,
    but use syntax similar to CongressPresenter and StatePresenter."""

    @classmethod
    def fetch(cls, latitude, longitude):
        return [cls.president(), cls.vice_president()]

    # return an ExecutivePresenter object with details for president
    @classmethod
    def president(cls):
        return ExecutivePresenter(bioguide_id="POTUS44",
                                  name="Barack Obama",
                                  title="President",
                                  constituency="USA",
                                  party="D",
                                  photo_url="http://a5.files.biography.com/image/upload/c_fill,cs_srgb,dpr_1.0,g_face,h_300,q_80,w_300/MTE4MDAzNDEwNzg5ODI4MTEw.jpg")

    @classmethod
    def vice_president(cls):
        return ExecutivePresenter(bioguide_id="VPforP44",
                                  name="Joe Biden",
                                  title="Vice President",
                                  constituency="USA",
                                  party="D",
                                  photo_url="https://upload.wikimedia.org/wikipedia/commons/e/ea/Official_portrait_of_Vice_President_Joe_Biden.jpg")

    def __init__(self, **dict):
        self.dict = dict

    def bioguide_id(self):
        return self.dict['bioguide_id']

    def name(self):
        return self.dict['name']

    def title(self):
        return self.dict['title']

    def constituency(self):
        return self.dict['constituency']

    def party(self):
        return self.dict['party']

    def photo_url(self):
        return self.dict['photo_url']





class PoliticianImporter(object):
    """Fetch data from API, then add or update local database."""


    def __init__(self, fetch):

        self.fetch = fetch
        self.alt_pic = PoliticianImporter.find_alt_pics()



    def add_or_update(self, latitude, longitude):
        people = self.fetch(latitude, longitude)
        for person in people:
            politician = Politician.query.filter(Politician.bioguide_id == person.bioguide_id()).first()
            if politician == None:
                politician = Politician(
                             bioguide_id= person.bioguide_id(),
                             name= person.name(),
                             title= person.title(),
                             constituency= person.constituency(),
                             party= person.party(),
                             photo_url= self.alt_pic.get(person.bioguide_id(), person.photo_url()),
                             )
                db.session.add(politician)
            else:
                politician.name = person.name()
                politician.party = person.party()
                politician.title = person.title()
                politician.constituency = person.constituency()
                politician.photo_url = self.alt_pic.get(person.bioguide_id(), person.photo_url())

        db.session.commit()
        bioguide_ids = [person.bioguide_id() for person in people]
        return Politician.query.filter(Politician.bioguide_id.in_(bioguide_ids)).all()

    @classmethod
    def find_alt_pics(cls):
        alt_pic = {}
        for row in open("static/photos.txt"):
            row = row.rstrip()
            alt_bioguide_id, alt_photo_url = row.split(" ")
            alt_pic[alt_bioguide_id] = alt_photo_url

        return alt_pic
