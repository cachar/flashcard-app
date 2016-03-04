import urllib2
from server import app
import unittest
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from model import connect_to_db, db

class MyTest(LiveServerTestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        connect_to_db(app, "postgresql:///flashcards_test")
        return app

    def test_student_can_review_notes(self):
        driver = webdriver.Chrome()
        driver.get(self.get_server_url())
        driver.find_element_by_css_selector('input[value="Notes"]').click()
        driver.find_element_by_link_text("Next").click()

        # page_contains("for")

        driver.find_element_by_link_text("Back").click()
        driver.close()

if __name__ == '__main__':
    unittest.main()
