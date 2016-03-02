import server
import unittest


class ServerTests(unittest.TestCase):
    """Tests for the server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True


    # Tests to make sure templates are rendered correctly

    def test_landing_page(self):

        result = self.client.get('/')
        
        self.assertEqual(result.status_code, 200)
        self.assertIn("Learn Your Representatives", result.data)

    def test_new_flashcards(self):
        
        result = self.client.get('/flashcards/new')

        self.assertEqual(result.status_code, 200)
        self.assertIn("party", result.data)

    # def test_create_card_deck(self):
    #     result = self.client.post('/card_decks',
    #                               data={'field': 'name',
    #                                     'scored': True,
    #                                     'latitude': '37.788666',
    #                                     'longitude': '-122.411462'},
    #                               follow_redirects=True)

    #     pass


class ServiceTests(unittest.TestCase):
    pass   


if __name__ == "__main__":
    unittest.main()
