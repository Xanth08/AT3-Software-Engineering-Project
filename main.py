from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random

app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret-key"

SONGS = [
    {"title": "Shape of You", "audio": "https://www.example.com/audio/shape_of_you.mp3"},
    {"title": "Blinding Lights", "audio": "https://www.example.com/audio/blinding_lights.mp3"},
    {"title": "Yesterday", "audio": "https://www.example.com/audio/yesterday.mp3"},
    # ... add as many as you like
]

@app.route("/")
def home():
    top_score = session.get("top_score", 0)
    return render_template("home.html", top_score=top_score)

@app.route("/start")
def start():
    session["round_score"] = 0
    session["playlist"] = random.sample(SONGS, len(SONGS))
    session["current_index"] = 0
    return redirect(url_for("game"))

@app.route("/game")
def game():
    # If we ran out of songs, reshuffle
    playlist = session.get("playlist", [])
    idx = session.get("current_index", 0)
    if idx >= len(playlist):
        session["playlist"] = random.sample(SONGS, len(SONGS))
        session["current_index"] = 0
        idx = 0

    song = session["playlist"][idx]
    return render_template("game.html", song_audio=song["audio"], song_title=song["title"])

@app.route("/submit_guess", methods=["POST"])
def submit_guess():
    data = request.get_json()
    guess = data.get("guess","").strip().lower()
    elapsed = float(data.get("elapsed", 0))  # time user took to guess (in seconds)

    # Current song
    idx = session.get("current_index", 0)
    playlist = session["playlist"]
    correct_title = playlist[idx]["title"].strip().lower()

    points_awarded = 0
    if guess == correct_title:
        # award max(0, 30 - elapsed) points, e.g., faster → more points
        points_awarded = max(0, int(30 - elapsed))
        session["round_score"] = session.get("round_score", 0) + points_awarded

    # advance to next song
    session["current_index"] = idx + 1

    return jsonify({
        "correct": guess == correct_title,
        "points": points_awarded,
        "round_score": session["round_score"]
    })

@app.route("/end_round", methods=["POST"])
def end_round():
    # Finalize top score
    round_score = session.get("round_score", 0)
    top = session.get("top_score", 0)
    if round_score > top:
        session["top_score"] = round_score
    # return to home
    return jsonify({
        "new_top": session.get("top_score", 0)
    })

if __name__ == "__main__":
    app.run(debug=True)