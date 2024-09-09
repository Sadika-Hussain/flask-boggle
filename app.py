from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pancakes'

boggle_game = Boggle()


@app.route('/')
def index():
    """
    Handle the route for the home page.
    - Generates a new boggle board and stores it in the session.
    - Retrieves the current highest score and play count from the session.
    - Renders the 'index.html' template with the board, high score, and play count.
    """
    board = boggle_game.make_board()
    session["board"] = board

    high_score = session.get('highest_score', 0)
    plays = session.get('play_count', 0)

    return render_template('index.html', board = board, high_score = high_score, plays = plays)

@app.route('/submit', methods = ['POST'])
def submit():
    """
    Handle the submission of a guess.
    - Retrieves the guessed word from the POST request.
    - Fetches the Boggle board from the session.
    - Checks if the guessed word is valid on the current board.
    - Returns the result of the guess as JSON.
    """
    data = request.get_json()
    guess = data.get('guess')
    board = session.get('board')
    result = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': f'{result}'})

@app.route('/complete', methods = ['POST'])
def complete():
    """
    Handle the completion of a game.
    - Receives the player's final score from the POST request.
    - Increments the play count in the session.
    - Updates the highest score in the session if the current score is higher.
    - Returns the score, updated play count, and high score as JSON.
    """
    data = request.get_json()

    score = data.get("score")

    play_count = session.get('play_count', 0)

    # Increment the play count 
    play_count += 1

    # Save the updated play_count back to the session
    session['play_count'] = play_count

    highest_score = session.get('highest_score', 0)

    if score > highest_score:
        highest_score = score

    session['highest_score'] = highest_score

    return jsonify({'score': f'{score}', 'playCount': f'{play_count}', 'highScore': highest_score})




