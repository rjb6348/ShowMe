class Event(object):
    """
    A class to represent an Event
    ...
    Attributes
    ----------
        event_json :
        event_name :
        artist_list :
        artist_ids :
        artist_searched :
        city :
        metro_id :
        date :
        time :
        date_time :
        performances :
        venue_name :
        venue_id :
        venue_uri :
        event_name :
        event_uri :
        event_id :
        headliner :
        artist_list :
        artist_ids :
    Methods
    -------
    set_searched_artist:
    get_city:
    get_metro_id:
    get_date:
    get_artists:
    get_artist_ids:
    get_performances:
    get_venue_name:
    get_venue_id:
    get_venue_uri:
    get_event_name:
    get_event_uri:
    get_headliner:
    get_searched_artist:
    get_event_json:
    get_event_id:
    get_num_performances:
    """

    def __init__(self, EventJson, *args, **kwargs):
        ''' Initialize object with Json returned from SongKick'''
        super().__init__(*args, **kwargs)
        self.event_json = EventJson
        self.event_name = None
        self.artist_list = []
        self.artist_ids = []
        self.artist_searched = None
        self.city = self.event_json['location']['city']
        self.metro_id = self.event_json['venue']['metroArea']['id']
        self.date = self.event_json['start']['date']
        self.time = self.event_json['start']['time']
        self.date_time = self.event_json['start']['datetime']
        self.performances = self.event_json['performance']
        self.venue_name = self.event_json['venue']['displayName']
        self.venue_id = self.event_json['venue']['id']
        self.venue_uri = self.event_json['venue']['uri']
        self.event_name = self.event_json['displayName']
        self.event_uri = self.event_json['uri']
        self.event_id = self.event_json['id']
        if len(self.event_json['performance']) > 0:
            self.headliner = self.event_json['performance'][0]['displayName']
            for artist_info in self.performances:
                self.artist_list.append(artist_info['displayName'])
            for artist_info in self.performances:
                self.artist_ids.append(artist_info['artist']['id'])
        else:
            self.headliner = []
            self.artist_list = []
            self.artist_ids = []

    def set_searched_artist(self, artist):
        ''' Set searched artist to associate if multiple at an event'''
        self.artist_searched = artist

    def get_city(self):
        ''' return the city of the event'''
        return self.city

    def get_metro_id(self):
        ''' return the metro_id of the event'''
        return self.metro_id

    def get_date(self):
        ''' return the date of the event'''
        return self.date

    def get_artists(self):
        ''' return the artists at the event'''
        return self.artist_list

    def get_artist_ids(self):
        ''' return the artist ids of the event'''
        return self.artist_ids

    def get_performances(self):
        ''' return the performances of the event'''
        return self.performances

    def get_venue_name(self):
        ''' return the venue name hosting the event'''
        return self.venue_name

    def get_venue_id(self):
        ''' return the venue id hosting the event'''
        return self.venue_id

    def get_venue_uri(self):
        ''' return the venue uri hosting the event'''
        return self.venue_uri

    def get_event_name(self):
        ''' return the event name'''
        return self.event_name

    def get_event_uri(self):
        ''' return the event uri'''
        return self.event_uri

    def get_headliner(self):
        ''' return the event headliner'''
        return self.headliner

    def get_searched_artist(self):
        ''' return the searched artist or headliner'''
        if self.artist_searched is not None:
            return self.artist_searched
        else:
            return self.get_headliner()

    def get_event_json(self):
        ''' return the original event json'''
        return self.event_json

    def get_event_id(self):
        ''' return the event id'''
        return self.event_id

    def get_num_performances(self):
        ''' return the number of performances at the event'''
        return len(self.performances)
