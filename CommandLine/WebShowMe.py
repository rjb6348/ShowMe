import os
import uuid
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
from pyzipcode import ZipCodeDatabase
import Artist
import ArtistList
import SongKickAPI
import Event
import EventList
from forms import BasicForm, ArtistResultForm, HomePageForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'

Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    uuid_ses = session.get('uuid')
    if uuid_ses is None:
        return_exp = caches_folder
    else:
        return_exp = caches_folder + session.get('uuid')
    return return_exp

@app.route('/')
def index():
    clear_search_keys()
    return render_template('HomePage.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/spotify_management', methods=['get', 'post'])
def spotify_management():
    if 'spotify' in session.keys():
        spotify = session["spotify"]
        me = spotify.me()
        return render_template('SpotifyManagementLoggedIn.html', name=me['display_name'])
    else:
        return render_template('SpotifyManagement.html')

@app.route('/basic_search', methods=['get', 'post'])
def basic_search():
    if "loc_id" in session.keys():
        del session["loc_id"]
    search = BasicForm(request.form)
    print("Search was run")
    print(session.keys())
    if request.method == 'POST':
        print("request was post")
        zip_result = search.searchZip.data.split("value")[-1]
        artist_result = search.searchArtist.data.split("value")[-1]
        if not zip_result == "" or not artist_result == "":
            song_kick = SongKickAPI.SongKickAPI()
            if not zip_result == "":
                zcdb = ZipCodeDatabase()
                try:
                    zip_int = zip_result
                    zipcode = zcdb[int(zip_int)]
                    print(zipcode.city, zipcode.state)
                    [loc_status, loc_id]  =  song_kick.find_city(zipcode.city, zipcode.state)
                    if loc_status.lower() == 'success':
                        session["loc_id"] = loc_id
                        session["city"] = zipcode.city
                    else:
                        message = "Location not found in database"
                except:
                    message = "Zip " + zip_result + " not found"
                    return render_template('SearchForm.html', form = search)
            if not artist_result == "":
                artist_name = artist_result
                [artist_search_status, artist_json] = song_kick.find_artist(artist_name)
                if artist_search_status.lower() == "success":
                    artist = Artist.Artist()
                    artist.add_songkick_data(artist_json)
                    artist_list = ArtistList.ArtistList()
                    artist_list.add_artist(artist)
                    session["artist_list"] = artist_list
                    print(artist_json)
                else:
                    message = "Artist " + artist_result + " Not Found"
                    return render_template('SearchForm.html', form = search)

            return basic_search_results()
    else:
        print(request.method)
    return render_template('SearchForm.html', form = search)

def clear_search_keys():
    if "artist_list" in session.keys():
        del session["artist_list"]
    if "loc_id" in session.keys():
        del session["loc_id"]
    if "city" in session.keys():
        del session["city"]

@app.route('/basic_search_results')
def basic_search_results():
    song_kick = SongKickAPI.SongKickAPI()
    print(session.keys())
    if "artist_list" in session.keys():
        if "loc_id" in session.keys():
            loc_id = session["loc_id"]
        else:
            loc_id = None
        artist_list = session['artist_list']
        event_list = EventList.EventList()
        for artist in artist_list.get_artists():
            [find_artist_events_status, events] = song_kick.find_artist_events(
                artist.get_display_name(), artist.get_artist_id(), metro_id=loc_id)
            if find_artist_events_status.lower() == "success":
                for event in events:
                    event_object = Event.Event(event)
                    event_object.set_searched_artist(artist.get_display_name())
                    event_list.add_event(event_object)
        if loc_id:
            loc_el = EventList.EventList()
            loc_el.create_event_list(event_list.get_events_by_metro_id(loc_id))
            loc_el.order_event_list_by_date()
            loc_el.print_events()
            session["event_list"] = loc_el
        else:
            session["event_list"] = event_list
        return redirect('/display_events')
    elif "loc_id" in session.keys():
        loc_id = session["loc_id"]
        [find_artist_events_status, events] = song_kick.find_location_events(
            session["city"], loc_id)
        event_list = EventList.EventList()
        if find_artist_events_status.lower() == "success":
            for event in events:
                event_list.add_event_json(event)
        event_list.print_events()
        session["event_list"] = event_list
        return redirect('/display_events')
    else:
        return "Unexpected hit"

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
    return redirect('/listening_history')

@app.route('/listening_history')
def listening_history():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/spotify_management')

    spotify = session['spotify']
    me = spotify.me()
    print(me)
    return render_template("listening_history.html",userName=me['display_name'])

@app.route("/go", methods=['POST'])
def go():
    data=request.form
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    artists_returned ={}
    if data['time_range'] == 'all_terms':
        artists_returned_short = spotify.current_user_top_artists(limit=data['num_tracks'], time_range='short_term')
        artists_returned_medium = spotify.current_user_top_artists(limit=data['num_tracks'], time_range='medium_term')
        artists_returned_long = spotify.current_user_top_artists(limit=data['num_tracks'], time_range='long_term')
        all_artists = artists_returned_short['items'] + artists_returned_medium['items'] + artists_returned_long['items']
        artists_returned['items'] = all_artists
    else:
        artists_returned = spotify.current_user_top_artists(limit=data['num_tracks'], time_range=data['time_range'])
    artist_list = ArtistList.ArtistList()
    for artist_json in artists_returned['items']:
        artist = Artist.Artist()
        artist.add_spotify_info(artist_json)
        artist_list.add_artist(artist)
    session['artist_list'] = artist_list
    return redirect('/disp_artists')

@app.route("/disp_artists", methods=['POST', 'GET'])
def disp_artists():
    search = ArtistResultForm(request.form)
    artist_list = session['artist_list']
    if request.method == 'POST':
        print("request was post")
        zip_result = search.searchZip.data.split("value")[-1]
        if not zip_result == "":
            song_kick = SongKickAPI.SongKickAPI()
            if not zip_result == "":
                zcdb = ZipCodeDatabase()
                try:
                    print("trying zip stuff")
                    zip_int = zip_result
                    zipcode = zcdb[int(zip_int)]
                    print(zipcode.city, zipcode.state)
                    [loc_status, loc_id]  =  song_kick.find_city(zipcode.city, zipcode.state)
                    if loc_status.lower() == 'success':
                        session["loc_id"] = loc_id
                        session["city"] = zipcode.city
                        return find_artists_songkick()
                    else:
                        message = "Location not found in database"
                        return render_template('displayArtists.html', artist_list=artist_list.get_artists_dictionaries(), form = search)
                except:
                    message = "Zip " + zip_result + " not found"
                    return render_template('displayArtists.html', artist_list=artist_list.get_artists_dictionaries(), form = search)
            return find_artists_songkick()
        else:
            return find_artists_songkick()
    else:
        print(request.method)
    return render_template('displayArtists.html', artist_list=artist_list.get_artists_dictionaries(), form = search)


@app.route("/find_artists_songkick", methods=['POST', 'GET'])
def find_artists_songkick():
    artist_list = session['artist_list']
    updated_artist_list = ArtistList.ArtistList()
    for artist in artist_list.get_artists():
        song_kick = SongKickAPI.SongKickAPI()
        [artist_search_status, artist_json] = song_kick.find_artist(artist.get_artist_name())
        if artist_search_status.lower() == "success":
            artist.add_songkick_data(artist_json)
            updated_artist_list.add_artist(artist)
    session['artist_list'] = updated_artist_list
    return redirect('/find_tours')

@app.route("/find_tours", methods=['POST', 'GET'])
def find_tours():
    date_range = None
    loc = None
    location_id = False
    artist_list = session['artist_list']
    event_list = EventList.EventList()
    print(session.keys())

    if "loc_id" in session.keys():
        location_id = session["loc_id"]

    for artist in artist_list.get_artists():
        song_kick = SongKickAPI.SongKickAPI()
        [find_artist_events_status, events] = song_kick.find_artist_events(
            artist.get_artist_name(), artist.get_artist_id(), date_range=date_range, metro_id=loc)
        if find_artist_events_status.lower() == "success":
            for event in events:
                event_object = Event.Event(event)
                event_object.set_searched_artist(artist.get_artist_name())
                event_list.add_event(event_object)

    if location_id is not False:
        loc_el = EventList.EventList()
        loc_el.create_event_list(event_list.get_events_by_metro_id(location_id))
        event_list = loc_el
    event_list.clean_event_list()
    event_list.order_event_list_by_date()
    session['event_list'] = event_list
    return redirect('/display_events')

@app.route("/display_events", methods=['POST', 'GET'])
def display_events():
    event_list = session['event_list']
    return render_template("displayEvents.html", event_list=event_list.get_event_dictionaries())


@app.route('/spotify_sign_out')
def spotify_sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        if session_cache_path() is not caches_folder:
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
