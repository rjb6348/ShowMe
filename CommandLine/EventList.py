import Event


class EventList(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eventJson = None
        self.Events = []

    def add_event_json(self, event):
        Ev = Event.Event(event)
        if Ev.get_num_performances() > 0:
            self.Events.append(Ev)
        # else debug statement I guess

    def add_event(self, event):
        if event.get_num_performances() > 0:
            self.Events.append(event)
        # else debug statement I guess

    def create_event_list(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                if event.get_num_performances() > 0:
                    self.Events.append(event)

    def create_event_list_json(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                Ev = Event.Event(event)
                if Ev.get_num_performances() > 0:
                    self.Events.append(Event.Event(event))

    def get_events_by_metro_id(self, metroID):
        returnEvents = []
        for event in self.Events:
            if event.get_metro_id() == metroID:
                returnEvents.append(event)
        return returnEvents

    def get_events_by_city(self, city):
        returnEvents = []
        for event in self.Events:
            if event.get_city().lower() == city.lower():
                returnEvents.append(event)
        return returnEvents

    def get_events_by_artist(self, artist):
        returnEvents = []
        for event in self.Events:
            if event.get_artists().lower() == artist.lower():
                returnEvents.append(event)
        return returnEvents

    def print_events(self):
        if len(self.Events) == 0:
            print("No Shows Found")
        for event in self.Events:
            print(event.get_searched_artist() + "\t will be coming to " + event.get_city() +
                  "\t on " + event.get_date() + "\t at the " + event.get_venue_name())

    def check_for_events(self):
        if len(self.Events) > 0:
            print("There are Events")

    def clean_event_list(self):
        tempEventList = []
        for x in self.Events:
            if x not in tempEventList:
                tempEventList.append(x)
        self.Events = tempEventList

    def get_event_by_id(self, id):
        for event in self.Events:
            if event.get_event_id() == id:
                return event
        return False

    def order_event_list_by_date(self):
        dateIdDict = {}
        tempEventList = []
        for event in self.Events:
            tempEventId = event.get_event_id()
            tempDate = event.get_date()
            dateIdDict[tempEventId] = tempDate
        sorteddates = dict(
            sorted(dateIdDict.items(), key=lambda item: item[1]))
        for id in sorteddates.keys():
            tempEventList.append(self.get_event_by_id(id))
        self.Events = tempEventList

    def get_events(self):
        return self.Events

    def get_events_in_time_window(self, startDate, endDate):
        tempEventList = []
        for event in self.Events:
            tempEventId = event.get_event_id()
            tempDate = event.get_date()
            if tempDate < endDate and tempDate > startDate:
                tempEventList.append(event)
        return tempEventList
