from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle
# from flask_debugtoolbar import DebugToolbar

app = Flask(__name__)
app.config["SECRET_KEY"] = "BOOGIE"
# app.debug = True

boggle_game = Boggle()
# debug = DebugToolbar(app)

@app.route("/")
def home():
    """making board"""
    boggle_board = boggle_game.make_board()
    session['board']= boggle_board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    return render_template("boggle.html", 
                            boggle_board=boggle_board,
                            highscore=highscore,
                            plays=plays)

@app.route("/word_check")
def check():
    """"Need to check if the work is in the dictionary"""

    word = request.arg["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result': response})

@app.route("/score", methods=["POST"])
def score():

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session['plays'] = plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
