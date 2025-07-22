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

    if 'score' not in session:
        session['score'] = 0
        session['current_round'] = 0
        session['total_rounds'] = session.get('rounds', 5)
        session['current_song'] = random.choice(songs)
    if request.method == 'POST':
        user_song_guess = request.form.get('song_guess')
        user_artist_guess = request.form.get('artist_guess')
        correct_song = session['current_song']['title']
        correct_artist = session['current_song']['artist']
        # Check guesses
        if user_song_guess.lower() == correct_song.lower():
            session['score'] += 10  # Award points for correct song
        if session.get('guess_artist', False) and user_artist_guess.lower() == correct_artist.lower():
            session['score'] += 10  # Award points for correct artist
        session['current_round'] += 1
        if session['current_round'] < session['total_rounds']:
            session['current_song'] = random.choice(songs)
        else:
            if session['score'] > session.get('high_score', 0):
                session['high_score'] = session['score']
            return redirect(url_for('home'))
    return render_template('game.html', song=session['current_song'], score=session['score'],
                           guess_artist=session.get('guess_artist', False))
if __name__ == '__main__':
    app.run(debug=True)