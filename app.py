from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret-key"

songs = [
    {"title": ["abcdefu"],      "file": "music/abcdefu-GAYLE.mp3",       "artist": ["GAYLE"]},
    {"title": ["Ark"],   "file": "music/Ark-Star_Party,Zookeepers.mp3",       "artist": ["Star Party","Zookeepers"]},
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
@app.route('/')
def home():
    return render_template('home.html', high_score=session.get('high_score', 0))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['guess_artist'] = 'guess_artist' in request.form
        session['rounds'] = int(request.form.get('rounds', 5))
        session['volume'] = float(request.form.get('volume', 1.0))
        return redirect(url_for('home'))
    
    # Add cancel button handling
    if request.args.get('cancel'):
        return redirect(url_for('home'))
        
    return render_template('settings.html', 
                         guess_artist=session.get('guess_artist', False),
                         rounds=session.get('rounds', 5), 
                         volume=session.get('volume', 1.0))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'game_started' not in session:
        initialize_game_session()
    
    if request.method == 'POST':
        if 'song_guess' in request.form:  # Check if a guess was made
            process_guess()
            return render_game_template()

        # If the next round button is clicked
        if 'next_round' in request.form:
            if session['current_round'] < session['total_rounds']:
                session['current_round'] += 1
                setup_new_round()
                # Clear feedback after moving to the next round
                session.pop('feedback', None)
                session.pop('song_guess', None)
                session.pop('artist_guess', None)
            else:
                end_game()
                return redirect(url_for('game_over'))
    
    return render_game_template()



def initialize_game_session():
    session['game_started'] = True
    session['score'] = 0
    session['current_round'] = 1
    session['total_rounds'] = session.get('rounds', 5)
    session['start_time'] = datetime.now().timestamp()
    session['current_song'] = random.choice(songs)

def process_guess():
    user_song_guess = request.form.get('song_guess')
    user_artist_guess = request.form.get('artist_guess')
    correct_titles = session['current_song']['title']
    correct_artists = session['current_song']['artist']

    # Calculate time taken
    time_taken = datetime.now().timestamp() - session['start_time']
    points_earned = 0

    # Base points (decrease with time)
    if any(user_song_guess.lower() == title.lower() for title in correct_titles):
        base_points = max(20 - int(time_taken), 5)  # Minimum 5 points
        session['score'] += base_points
        points_earned += base_points
    
    # Bonus artist points
    if session.get('guess_artist', False) and any(user_artist_guess.lower() == artist.lower() for artist in correct_artists):
        session['score'] += 10
        points_earned += 10

    # Store feedback in session
    session['feedback'] = {
        'correct_title': correct_titles[0],
        'correct_artist': correct_artists[0] if session.get('guess_artist', False) else None,
        'points_earned': points_earned
    }
    
    session['song_guess'] = user_song_guess
    session['artist_guess'] = user_artist_guess


def setup_new_round():
    session['current_song'] = get_new_song()
    session['start_time'] = datetime.now().timestamp()

def get_new_song():
    remaining_songs = [s for s in songs if s != session['current_song']]
    return random.choice(remaining_songs) if remaining_songs else random.choice(songs)

def end_game():
    if session['score'] > session.get('high_score', 0):
        session['high_score'] = session['score']
    clear_game_session()

def clear_game_session():
    for key in ['game_started', 'current_round', 'total_rounds', 'current_song', 'start_time', 'feedback']:
        session.pop(key, None)

def render_game_template():
    feedback = session.get('feedback', None)
    return render_template('game.html', 
                         song=session['current_song'],
                         score=session['score'],
                         current_round=session['current_round'],
                         total_rounds=session['total_rounds'],
                         guess_artist=session.get('guess_artist', False),
                         feedback=feedback)


@app.route('/next-round')
def next_round():
    return redirect(url_for('game'))

@app.route('/game-over')
def game_over():
    final_score = session.get('score', 0)
    return render_template('results.html', 
                           final=final_score,
                           high_score=session.get('high_score', 0))

if __name__ == '__main__':
    app.run(debug=True)
