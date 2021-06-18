import Event
class EventList(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eventJson = None
        self.Events = []

    def addEventJson(self, event):
        Ev = Event.Event(event)
        if Ev.getNumPerformances() > 0:
            self.Events.append(Ev)
        #else debug statement I guess

    def addEvent(self, event):
        if event.getNumPerformances() > 0:
            self.Events.append(event)
        #else debug statement I guess

    def createEventList(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                if event.getNumPerformances() > 0:
                    self.Events.append(event)

    def createEventListJson(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                Ev = Event.Event(event)
                if Ev.getNumPerformances() > 0:
                    self.Events.append(Event.Event(event))

    def getEventsByMetroId(self, metroID):
        returnEvents = []
        for event in self.Events:
            if event.getMetroId() == metroID:
                returnEvents.append(event)
        return returnEvents

    def getEventsByCity(self, city):
        returnEvents = []
        for event in self.Events:
            if event.getCity().lower() == city.lower():
                returnEvents.append(event)
        return returnEvents

    def getEventsByArtist(self, artist):
        returnEvents = []
        for event in self.Events:
            if event.getArtists().lower() == artist.lower():
                returnEvents.append(event)
        return returnEvents

    def printEvents(self):
        if len(self.Events) == 0:
            print("No Shows Found")
        for event in self.Events:
            print(event.getSearchedArtist() + " will be coming to " + event.getCity() + " on " + event.getDate() + " at the " + event.getVenueName())

    def checkforEvents(self):
        if len(self.Events)>0:
            print("There are Events")

    def cleanEventList(self):
        tempEventList = []
        for x in self.Events:
            if x not in tempEventList:
                tempEventList.append(x)
        self.Events = tempEventList

    def getEventById(self, id):
        for event in self.Events:
            if event.getEventId() == id:
                return event
        return False

    def orderEventListByDate(self):
        dateIdDict = {}
        tempEventList = []
        for event in self.Events:
            tempEventId = event.getEventId()
            tempDate = event.getDate()
            dateIdDict[tempEventId] = tempDate
        sorteddates = dict(sorted(dateIdDict.items(), key=lambda item : item[1]))
        for id in sorteddates.keys():
            tempEventList.append(self.getEventById(id))
        self.Events = tempEventList

    def getEvents(self):
        return self.Events

    def getEventsinTimeWindow(self, startDate, endDate):
        tempEventList = []
        for event in self.Events:
            tempEventId = event.getEventId()
            tempDate = event.getDate()
            if tempDate < endDate and tempDate > startDate:
                tempEventList.append(event)
        return tempEventList

    



