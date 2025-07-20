from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import random

app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret-key"

# 1) Configure your songs here by filename and human‐readable title
SONGS = [
    {"title": ["abcdefu"],      "file": "music/abcdefu-GAYLE.mp3",       "artists": ["GAYLE"]},
    {"title": ["Ark"],   "file": "music/Ark-Star_Party,Zookeepers.mp3",       "artists": ["Star Party","Zookeepers"]},
    {"title": ["Because of You"],         "file": "music/Because_of_You-Kelly_Clarkson.mp3",      "artist": ["Kelly Clarkson"]},
    {"title": ["Cipher"],         "file": "music/Cipher-Kevin MacLeod.mp3",      "artist": ["Kevin MacLeod"]},
    {"title": ["Colorblind"],         "file": "music/Colorblind-Panda_Eyes.mp3",      "artist": ["Panda Eyes"]},
    {"title": ["Come Alive"],         "file": "music/Come Alive-Hugh Jackman.mp3",      "artist": ["Hugh Jackman","Keala Settle","Daniel Everidge","Zendaya"]},
    {"title": ["Congratulations"],         "file": "music/Congratulations-Post_Malone,Quavo.mp3",      "artist": ["Post Malone","Quavo"]},
    {"title": ["Copacabana"],         "file": "music/Copacabana-Barry_Manilow.mp3",      "artist": ["Barry Manilow"]},
    {"title": ["Dancing With Your Ghost"],         "file": "music/Dancing_With_Your_Ghost-Sasha_Alex_Sloan.mp3",      "artist": ["Sasha Alex Sloan"]},
    {"title": ["Daycare Theme"],         "file": "music/Daycare_Theme-Allen_Simpson.mp3",      "artist": ["Allen Simpson"]},
    {"title": ["Daylight"],         "file": "music/Daylight-David_Kushner.mp3",      "artist": ["David Kushner"]},
    {"title": ["Don't You Worry Child","Dont You Worry Child"],         "file": "music/Don't_You_Worry_Child-Swedish_House_Mafia,John_Martin.mp3",      "artist": ["Swedish House Mafia","John Martin"]},
    {"title": ["Drop into the Pit"],         "file": "music/Drop_into_the_Pit-Tryhardninja.mp3",      "artist": ["Tryhardninja"]},
    {"title": ["Far Away from Home"],         "file": "music/Far_Away_from_Home-Paratone,Katrine_Stenbekk.mp3",      "artist": ["Paratone","Katrine Stenbekk"]},
    {"title": ["Feel Good"],         "file": "music/Feel_Good-Syn_Cole.mp3",      "artist": ["Syn Cole"]},
    {"title": ["Fields of Gold"],         "file": "music/Fields_of_Gold-Sting.mp3",      "artist": ["Sting"]},
    {"title": ["Fresh Rain"],         "file": "music/Fresh_Rain-LSPLASH.mp3",      "artist": ["LSPLASH"]},
    {"title": ["Ghost"],         "file": "music/Ghost-Justin_Bieber.mp3",      "artist": ["Justin Bieber"]},
    {"title": ["Go!","Go"],         "file": "music/Go!-Teen Titans Go!.mp3",      "artist": ["Teen Titans Go!","Greg Cipes","Scott Menville","Khary Payton","Tara Strong","Hynden Walch"]},
    {"title": ["Heather"],         "file": "music/Heather-Conan_Gray.mp3",      "artist": ["Conan Gray"]},
    {"title": ["Hexagon Force"],         "file": "music/Hexagon_Force-Waterflame.mp3",      "artist": ["Waterflame"]},
    {"title": ["Hey Mama"],         "file": "music/Hey_Mama-David Guetta,AFROJACK,Bebe.mp3",      "artist": ["David Guetta","AFROJACK","Bebe"]},
    {"title": ["I Gotta Feeling","I Got A Feeling"],         "file": "music/I_Gotta_Feeling-Black_Eyed_Peas.mp3",      "artist": ["Black Eyed Peas"]},
    {"title": ["La Da Dee"],         "file": "music/La_Da_Dee-Cody_Simpson.mp3",      "artist": ["Cody Simpson"]},
    {"title": ["Look at Me Now"],         "file": "music/Look_at_Me_Now-Tryhardninja,Skyfixing.mp3",      "artist": ["Tryhardninja, Skyfixing"]},
    {"title": ["Lost Woods"],         "file": "music/Lost_Woods-Crazyblox.mp3",      "artist": ["Crazyblox"]},
    {"title": ["Monument"],         "file": "music/Monument-Royksopp,Robyn.mp3",      "artist": ["Royksopp","Robyn"]},
    {"title": ["Numb Little Bug"],         "file": "music/Numb_Little_Bug-Em_Beihold.mp3",      "artist": ["Em Beihold"]},
    {"title": ["One Last Time"],         "file": "music/One_Last_Time-Ariana_Grande.mp3",      "artist": ["Ariana Grande"]},
    {"title": ["Only Girl","Only Girl In The World","Only Girl (In The World)"],         "file": "music/Only_Girl_(In_The_World)-Rihanna.mp3",      "artist": ["Rihanna"]},
    {"title": ["Open The Door"],         "file": "music/Open_The_Door-LongestSoloEver,DayumDahlia.mp3",      "artist": ["LongestSoloEver","DayumDahlia"]},
    {"title": ["Right Round"],         "file": "music/Right_Round-Flo_Rida,Kesha.mp3",      "artist": ["Flo Rida, Kesha"]},
    {"title": ["Riptide"],         "file": "music/Riptide-Vance_Joy.mp3",      "artist": ["Vance Joy"]},
    {"title": ["Rise"],         "file": "music/Rise-Jonas_Blue,Jack_&_Jack.mp3",      "artist": ["Jonas Blue","Jack and Jack","Jack & Jack"]},
    {"title": ["rockstar"],         "file": "music/rockstar-Post_Malone,21_Savage.mp3",      "artist": ["Post Malone","21 Savage"]},
    {"title": ["Seven"],         "file": "music/Seven-Jung_Kook,Latto.mp3",      "artist": ["Jung Kook","Latto"]},
    {"title": ["Shadow"],         "file": "music/Shadow-Bossfight,JT_Roach,RUNN.mp3",      "artist": ["Bossfight","JT_Roach","RUNN"]},
    {"title": ["Skyfall"],         "file": "music/Skyfall-Adele.mp3",      "artist": ["Adele"]},
    {"title": ["Starshine Beach Galaxy"],         "file": "music/Starshine_Beach_Galaxy-Arcade_Player.mp3",      "artist": ["Mahito Yokota"]},
    {"title": ["Starving"],         "file": "music/Starving-Hailee_Steinfeld,Grey,Zedd.mp3",      "artist": ["Hailee Steinfeld","Grey","Zedd"]},
    {"title": ["Strawberry Fields Forever"],         "file": "music/Strawberry_Fields_Forever-The_Beatles.mp3",      "artist": ["The Beatles"]},
    {"title": ["Take Me Home, Country Roads", "Take Me Home Country Roads"],         "file": "music/Take_Me_Home,Country_Roads-John_Denver.mp3",      "artist": ["John Denver"]},
    {"title": ["The Greatest Show"],         "file": "music/The_Greatest_Show-Hugh Jackman.mp3",      "artist": ["Hugh Jackman","Keala Settle","Zac Efron","Zendaya"]},
    {"title": ["The Qantas Soundtrack","Qantas Soundtrack"],         "file": "music/The_Qantas_Soundtrack-Qantas,HaydnWalker.mp3",      "artist": ["Qantas","HaydnWalker"]},
    {"title": ["Throwback Galaxy"],         "file": "music/Throwback_Galaxy-Arcade_Player.mp3",      "artist": ["Koji Kondo"]},
    {"title": ["Trailer Theme","Trailer Theme-Extended","Trailer Theme Extended"],         "file": "music/Trailer_Theme-Extended-Mekbok.mp3",      "artist": ["Mekbok"]},
    {"title": ["Trailer Theme","Trailer Theme Remix","Trailer Theme - Remix"],         "file": "music/Trailer_Theme-Remix-LSPLASH.mp3",      "artist": ["LSPLASH"]},
    {"title": ["Tremble"],         "file": "music/Tremble-Nicole_Millar.mp3",      "artist": ["Nicole Millar"]},
    {"title": ["Uptown Girl"],         "file": "music/Uptown_Girl-Billy_Joel.mp3",      "artist": ["Billy Joel"]},
    {"title": ["We Don't Talk About Bruno","We Dont Talk About Bruno"],         "file": "music/We_Don't_Talk_About_Bruno-Carolina_Gaitan,Adassa,Rhenzy_Feliz,Diane_Guerrero,.mp3",      "artist": ["Carolina Gaitan, Adassa, Rhenzy Feliz, Diane Guerrero"]},
    {"title": ["Where Have You Been"],         "file": "music/Where_Have_You_Been-Rihanna.mp3",      "artist": ["Rihanna"]},
    {"title": ["Windfall"],         "file": "music/Windfall-TheFatRat.mp3",      "artist": ["TheFatRat"]},



]

@app.route("/")
def home():
    top_score = session.get("top_score", 0)
    return render_template("home.html", top_score=top_score)

@app.route("/start")
def start():
    # Reset round state
    session["round_score"] = 0
    session["playlist"]    = random.sample(SONGS, len(SONGS))
    session["current_index"] = 0
    return redirect(url_for("game"))

@app.route("/game")
def game():
    # If we’ve exhausted the playlist, reshuffle
    playlist = session.get("playlist", [])
    idx      = session.get("current_index", 0)
    if idx >= len(playlist):
        session["playlist"]    = random.sample(SONGS, len(SONGS))
        session["current_index"] = 0
        idx = 0

    song_meta = session["playlist"][idx]
    audio_url = url_for("static", filename=f"music/{song_meta['file']}")

    return render_template(
        "game.html",
        song_audio=audio_url,
        song_title=song_meta["title"]
    )

@app.route("/submit_guess", methods=["POST"])
def submit_guess():
    data    = request.get_json()
    guess   = data.get("guess", "").strip().lower()
    elapsed = float(data.get("elapsed", 0))

    idx          = session.get("current_index", 0)
    playlist     = session.get("playlist", [])
    correct_title = playlist[idx]["title"].strip().lower()

    points_awarded = 0
    if guess == correct_title:
        # e.g. award up to 30 − elapsed seconds
        points_awarded = max(0, int(30 - elapsed))
        session["round_score"] = session.get("round_score", 0) + points_awarded

    session["current_index"] = idx + 1

    return jsonify({
        "correct":     guess == correct_title,
        "points":      points_awarded,
        "round_score": session.get("round_score", 0)
    })

@app.route("/end_round", methods=["POST"])
def end_round():
    round_score = session.get("round_score", 0)
    top_score   = session.get("top_score", 0)

    if round_score > top_score:
        session["top_score"] = round_score

    return jsonify({ "new_top": session.get("top_score", 0) })

if __name__ == "__main__":
    app.run(debug=True)
