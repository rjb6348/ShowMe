import Event
import SongKickAPI
import ShowMeUtilities as smUtil
import EventList
import Artist
import ArtistList


def main():
    music_library = None
    location = None

    search_type = smUtil.prompt_for_search_type()
    if search_type is False:
        print("Crash Here")

    music_library = None
    song_kick = SongKickAPI.SongKickAPI()

    if search_type == 3:
        music_library = smUtil.setup_music_library()
        if music_library is False:
            print("Fail")

    location = smUtil.check_to_query_location(search_type, song_kick)

    date_range = smUtil.query_date_range()

    returned_input = smUtil.create_search_type_query(search_type)

    events = search(search_type, returned_input, location, song_kick, music_library, date_range)

    #displayEvents = (events, input)


def search(search_type, input_arg, location, song_kick, music_library, date_range):
    if search_type == 1:
        events = artist_search(input_arg, location, song_kick, date_range)
    elif search_type == 2:
        events = location_search(location, song_kick, date_range)
    elif search_type == 3:
        events = library_search(input_arg, location, song_kick, music_library, date_range)
    return events


def artist_search(input_arg, location, song_kick, date_range):
    [artist_search_status, artist_json] = song_kick.find_artist(input_arg)
    if date_range[0] is False:
        dr = None
    else:
        dr = date_range
    if location[1] is False:
        loc = None
    else:
        loc = location[1]

    if artist_search_status.lower() == "success":
        artist = Artist.Artist()
        artist.add_songkick_data(artist_json)
        event_list = EventList.EventList()
        [find_artist_events_status, events] = song_kick.find_artist_events(
            input_arg, artist.get_artist_id(), date_range=dr, metro_id=loc)
        if find_artist_events_status.lower() == "success":
            for event in events:
                event_object = Event.Event(event)
                event_object.set_searched_artist(artist.get_disply_name())
                event_list.add_event(event_object)
        if location[1] is not False:
            loc_el = EventList.EventList()
            loc_el.create_event_list(event_list.get_events_by_metro_id(location[1]))
            loc_el.print_events()
        else:
            event_list.print_events()
    else:
        print(artist_json)


def location_search(location, song_kick, date_range):
    print("Location Search")
    if date_range[0] is False:
        dr = None
    else:
        dr = date_range
    [find_artist_events_status, events] = song_kick.find_location_events(
        location[0][0], location[1], date_range=dr)
    event_list = EventList.EventList()
    if find_artist_events_status.lower() == "success":
        for event in events:
            event_list.add_event_json(event)
    event_list.print_events()


def library_search(input_arg, location, song_kick, music_library, date_range):
    print("Library Search")
    location_id = location[1]
    time_range = input_arg
    if date_range[0] is False:
        dr = None
    else:
        dr = date_range
    if location[1] is False:
        loc = None
    else:
        loc = location[1]
    top_artists = [[] for i in time_range]
    top_artist_status = [[] for i in time_range]
    print("Pulling Artists")
    for time_range_index in range(0, len(time_range)):
        [top_artists[time_range_index], top_artist_status[time_range_index]] = music_library.pull_user_top_artists(
            limit=50, time_range=time_range[time_range_index])
    artist_list = ArtistList.ArtistList()
    for time_range_index in range(0, len(top_artist_status)):
        if top_artist_status[time_range_index].lower() == 'success':
            print("Your Top artist of: " + time_range[time_range_index])
            for artist_json in top_artists[time_range_index]['items']:
                artist = Artist.Artist()
                artist.add_spotify_info(artist_json)
                artist_list.add_artist(artist)

    print("Finding Artist Info")
    new_artist_list = ArtistList.ArtistList()
    for artist in artist_list.get_artists():
        [artist_search_status, artist_json] = song_kick.find_artist(
            artist.get_artist_name())
        if artist_search_status == "Success":
            artist.add_songkick_data(artist_json)
            new_artist_list.add_artist(artist)

    print("Finding Artist Events")
    event_list = EventList.EventList()
    for artist in new_artist_list.get_artists():
        song_kick = SongKickAPI.SongKickAPI()
        [find_artist_events_status, events] = song_kick.find_artist_events(
            artist.get_artist_name(), artist.get_artist_id(), date_range=dr, metro_id=loc)
        if find_artist_events_status == "Success":
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
    event_list.print_events()


if __name__ == "__main__":
    main()
