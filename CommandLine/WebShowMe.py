import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import uuid
import Artist
import ArtistList
import SongKickAPI
import Event
import EventList

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/')
def index():
    return f'<a href="/basic_search">[Basic Search]<a/></h2>' \
           f'<a href="/spotify_login">[Login with Spotify]</a> | ' \

@app.route('/spotify_login')
def spotify_login():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-library-read user-top-read',
                                                cache_handler=cache_handler, 
                                                show_dialog=True,
                                                redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI", "8080")+'/spotify_login')

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        #print(request.args.get("code"))
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/spotify_login')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    session['spotify'] = spotify
    return redirect('/spotify_interactions')

@app.route('/spotify_interactions')
def spotify_interactions():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = session['spotify']

    return render_template("spotify_interactions.html",userName=spotify.me()['display_name'])

@app.route("/go", methods=['POST'])
def go():
    data=request.form
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    artists_returned = spotify.current_user_top_artists(limit=data['num_tracks'], time_range=data['time_range'])
    artist_list = ArtistList.ArtistList()
    for artist_json in artists_returned['items']:
        artist = Artist.Artist()
        artist.add_spotify_info(artist_json)
        artist_list.add_artist(artist)
    session['artist_list'] = artist_list
    return redirect('/disp_artists')

@app.route("/disp_artists", methods=['POST', 'GET'])
def disp_artist():
    artist_list = session['artist_list']
    return render_template("displayArtists.html",artist_list=artist_list.get_artists_dictionaries())

@app.route("/find_artists_songkick", methods=['POST', 'GET'])
def find_artists_songkick():
    artist_list = session['artist_list']
    updated_artist_list = ArtistList.ArtistList()
    for artist in artist_list.get_artists():
        sk = SongKickAPI.SongKickAPI()
        [artist_search_status, artist_json] = sk.findArtist(artist.get_artist_name())
        if artist_search_status == "Success":
            artist.add_songkick_data(artist_json)
            updated_artist_list.add_artist(artist)
    session['artist_list'] = updated_artist_list
    return redirect('/find_tours')

@app.route("/find_tours", methods=['POST', 'GET'])
def find_tours():
    dr = None
    loc = None
    location_id = False
    artist_list = session['artist_list']
    updated_artist_list = ArtistList.ArtistList()
    EL = EventList.EventList()
    for artist in artist_list.get_artists():
        sk = SongKickAPI.SongKickAPI()
        [find_artist_events_status, events] = sk.findArtistEvents(
            artist.get_artist_name(), artist.get_artist_id(), dateRange=dr, metroId=loc)
        if find_artist_events_status == "Success":
            for event in events:
                EO = Event.Event(event)
                EO.set_searched_artist(artist.get_artist_name())
                EL.add_event(EO)

    if location_id is not False:
        locEL = EventList.EventList()
        locEL.create_event_list(EL.get_events_by_metro_id(location_id))
        EL = locEL
    EL.clean_event_list()
    EL.order_event_list_by_date()
    session['event_list'] = EL
    return redirect('/display_events')

@app.route("/display_events", methods=['POST', 'GET'])
def display_events():
    EL = session['event_list']
    return render_template("displayEvents.html", event_list=EL.get_event_dictionaries())


@app.route('/spotify_sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')

@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()



if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", "8080").split(":")[-1])))