from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """
        Set up the test client before each test.
        """
        self.client = app.test_client()
        self.client.testing = True

    def test_index_route(self):
        """
        Test the index route.
        - Ensures the response is successful (status code 200).
        - Checks if the correct template is rendered.
        - Verifies that session variables (board, high_score, plays) are set correctly.
        """
        with self.client as client:

            # Simulate a GET request to the index route
            response = client.get('/')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsInstance(session['board'], list)  
            self.assertNotIn('highest_score', session)
            self.assertNotIn('play_count', session)
            self.assertIn(b'<title>Boggle Game</title>', response.data)
    
    def test_submit_valid_guess(self):
        """
        Test the /submit route with a valid guess.
        - Simulates a game board and submits a valid word.
        - Verifies that the result is 'ok' for a valid guess.
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['N', 'J', 'B', 'H', 'M'], 
                    ['C', 'I', 'F', 'O', 'A'], 
                    ['Z', 'O', 'J', 'P', 'R'], 
                    ['Z', 'S', 'B', 'X', 'C'], 
                    ['L', 'P', 'C', 'A', 'D']]
                
            response = client.post('/submit', json={'guess': 'sob'})

            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertEqual(data['result'], 'ok')

    def test_submit_invalid_guess(self):
        """
        Test the /submit route with an invalid guess (not on the board).
        - Simulates a game board and submits a word not found on the board.
        - Verifies that the result is 'not-on-board' for an invalid guess.
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['N', 'J', 'B', 'H', 'M'], 
                    ['C', 'I', 'F', 'O', 'A'], 
                    ['Z', 'O', 'J', 'P', 'R'], 
                    ['Z', 'S', 'B', 'X', 'C'], 
                    ['L', 'P', 'C', 'A', 'D']]
                
            response = client.post('/submit', json={'guess': 'word'})

            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertEqual(data['result'], 'not-on-board')

    def test_submit_not_english_word(self):
        """
        Test the /submit route with a non-English word.
        - Simulates a game board and submits a non-English word.
        - Verifies that the result is 'not-word' for an invalid word.
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ['N', 'J', 'B', 'H', 'M'], 
                    ['C', 'I', 'F', 'O', 'A'], 
                    ['Z', 'O', 'J', 'P', 'R'], 
                    ['Z', 'S', 'B', 'X', 'C'], 
                    ['L', 'P', 'C', 'A', 'D']]
                
            response = client.post('/submit', json={'guess': 'xyz'})

            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertEqual(data['result'], 'not-word')

    def test_complete_route(self):
        """
        Test the /complete route to handle game completion.
        - Simulates a session with a play count and high score.
        - Submits a final score and verifies that the play count increments and the high score updates.
        """
        # Create a POST request to the /complete route
        with app.test_client() as client:
            # Simulate existing session data for play count and high score
            with client.session_transaction() as sess:
                sess['play_count'] = 3  
                sess['highest_score'] = 10  

            response = client.post('/complete', json={'score': 15})

            self.assertEqual(response.status_code, 200)

             # Parse the JSON response and check the values
            response_data = response.get_json()
            self.assertEqual(response_data['score'], '15')
            self.assertEqual(response_data['playCount'], '4')  # play_count incremented by 1
            self.assertEqual(response_data['highScore'], 15)   # highest score updated

          
    