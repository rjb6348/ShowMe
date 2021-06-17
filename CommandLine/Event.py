class Event(object):

    def __init__(self, EventJson, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eventJson = EventJson
        self.eventName = None
        self.ArtistList = []
        self.ArtistIds = []
        self.city = self.eventJson['location']['city']
        self.metroId = self.eventJson['venue']['metroArea']['id']
        self.date = self.eventJson['start']['date']
        self.time = self.eventJson['start']['time']
        self.dateTime = self.eventJson['start']['datetime']
        self.performances = self.eventJson['performance']
        self.venueName = self.eventJson['venue']['displayName']
        self.venueId = self.eventJson['venue']['id']
        self.venueURI = self.eventJson['venue']['uri']
        self.eventName = self.eventJson['displayName']
        self.eventURI = self.eventJson['uri']
        self.headliner = self.eventJson['performance'][0]['displayName']
        self.EventId = self.eventJson['id']
        for artistInfo in self.performances:
            self.ArtistList.append(artistInfo['displayName'])

        for artistInfo in self.performances:
            self.ArtistIds.append(artistInfo['artist']['id'])

    def getCity(self):
        return self.city

    def getMetroId(self):
        return self.metroId

    def getDate(self):
        return self.date

    def getArtists(self):
        return self.ArtistList

    def getArtistIds(self):
        return self.ArtistIds

    def getPerformances(self):
        return self.performances

    def getVenueName(self):
        return self.venueName

    def getVenueId(self):
        return self.venueId

    def getVenueURI(self):
        return self.venueURI

    def getEventName(self):
        return self.eventName

    def getEventURI(self):
        return self.eventURI

    def getHeadliner(self):
        return self.headliner

    def getEventJson(self):
        return self.eventJson

    def getEventId(self):
        return self.EventId