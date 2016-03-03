from server import app
from model import *
import unittest


class FlashcardTests(unittest.TestCase):
    """Tests for the server."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data_high_scores()


    # Tests to make sure templates are rendered correctly

    def test_landing_page(self):

        result = self.client.get('/')
        
        self.assertEqual(result.status_code, 200)
        self.assertIn("House of Cards", result.data)

    def test_new_flashcards(self):
        
        result = self.client.get('/flashcards/new')

        self.assertEqual(result.status_code, 200)
        self.assertIn("party", result.data)

    def test_create_card_deck(self):
        pass

        # result = self.client.post('/card_decks',
        #                           data={'field': 'name',
        #                                 'scored': True,
        #                                 'latitude': '37.788666',
        #                                 'longitude': '-122.411462'},
        #                           follow_redirects=True)

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_top_five_scores(self):

        top_five = HighScore.top_five_scores()

        self.assertEqual(len(top_five), 5)

        






if __name__ == "__main__":
    unittest.main()
