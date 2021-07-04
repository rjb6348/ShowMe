import pandas as pd
import Event
import SongKickAPI
import ShowMeUtilities as smUtil
import EventList
import Artist
import ArtistList


def main():
    ml = None
    location = None

    search_type = smUtil.prompt_for_search_type()
    if search_type is False:
        print("Crash Here")

    ml = None
    sk = SongKickAPI.SongKickAPI()

    if search_type == 3:
        ml = smUtil.setup_music_library()
        if ml is False:
            print("Fail")

    location = smUtil.check_to_query_location(search_type, sk)

    date_range = smUtil.query_date_range()

    input = smUtil.create_search_type_query(search_type)

    events = search(search_type, input, location, sk, ml, date_range)

    #displayEvents = (events, input)


def search(search_type, input, location, sk, ml, date_range):
    if search_type == 1:
        events = artist_search(input, location, sk, date_range)
    elif search_type == 2:
        events = location_search(input, location, sk, date_range)
    elif search_type == 3:
        events = library_search(input, location, sk, ml, date_range)
    return events


def artist_search(input, location, sk, date_range):
    [artist_search_status, artist_json] = sk.findArtist(input)
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
        EL = EventList.EventList()
        [find_artist_events_status, events] = sk.findArtistEvents(
            input, artist.get_artist_id(), dateRange=dr, metroId=loc)
        if find_artist_events_status.lower() == "success":
            for event in events:
                EO = Event.Event(event)
                EO.set_searched_artist(artist.get_disply_name())
                EL.add_event(EO)
        if location[1] is not False:
            locEL = EventList.EventList()
            locEL.create_event_list(EL.get_events_by_metro_id(location[1]))
            locEL.print_events()
        else:
            EL.print_events()
    else:
        print(artist_json)


def location_search(input, location, sk, date_range):
    print("Location Search")
    if date_range[0] is False:
        dr = None
    else:
        dr = date_range
    [find_artist_events_status, events] = sk.findLocationEvents(
        location[0][0], location[1], dateRange=dr)
    EL = EventList.EventList()
    if find_artist_events_status == "Success":
        for event in events:
            EL.add_event_json(event)
    EL.print_events()


def library_search(input, location, sk, ml, date_range):
    print("Library Search")
    location_id = location[1]
    City = location[0][0]
    time_range = input
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
    artist_ids, artist_names, artist_events, status, status_code = [], [], [], [], []
    print("Pulling Artists")
    for tr in range(0, len(time_range)):
        [top_artists[tr], top_artist_status[tr]] = ml.pullUserTopArtists(
            limit=50, time_range=time_range[tr])
    artist_list = ArtistList.ArtistList()
    for tr in range(0, len(top_artist_status)):
        if top_artist_status[tr].lower() == 'success':
            print("Your Top artist of: " + time_range[tr])
            for artist_json in top_artists[tr]['items']:
                artist = Artist.Artist()
                artist.add_spotify_info(artist_json)
                artist_list.add_artist(artist)


    print("Finding Artist Info")
    new_artist_list = ArtistList.ArtistList()
    for artist in artist_list.get_artists():
        [artist_search_status, artist_json] = sk.findArtist(artist.get_artist_name())
        if artist_search_status == "Success":
            artist.add_songkick_data(artist_json)
            new_artist_list.add_artist(artist)

    print("Finding Artist Events")
    EL = EventList.EventList()
    for artist in new_artist_list.get_artists():
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
    EL.print_events()
    '''
    for rank, [artist, curr_status, curr_code, artist_id] in df.iterrows():
        if curr_status == "Success":
            event_list = []
            [find_artist_events_status, events] = sk.findArtistEvents(
                artist, artist_id, dateRange=dr, metroId=loc)
            if find_artist_events_status == "Success":
                for event in events:
                    EO = Event.Event(event)
                    EO.set_searched_artist(artist)
                    event_list.append(EO)
                    EL.add_event(EO)
            else:
                event_list.append(status)
                df.loc[rank, 'status'] = find_artist_events_status
                df.loc[rank, 'statusCode'] = events
            artist_events.append(event_list)
        else:
            artist_events.append(None)

    if location_id is not False:
        locEL = EventList.EventList()
        locEL.create_event_list(EL.get_events_by_metro_id(location_id))
        EL = locEL

    EL.clean_event_list()
    EL.order_event_list_by_date()
    print("Ordered and sanitized")
    EL.print_events()
    '''

if __name__ == "__main__":
    main()
