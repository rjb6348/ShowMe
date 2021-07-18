import Event


class EventList(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_json = None
        self.Events = []
        self.event_dictionaries = []

    def update_event_dictionaries(self, event):
        self.event_dictionaries.append(event.get_event_dict())

    def reset_event_dict(self):
        self.event_dictionaries.clear()
        for event in self.Events:
            self.update_event_dictionaries(event)

    def add_event_json(self, event):
        Ev = Event.Event(event)
        if Ev.get_num_performances() > 0:
            self.Events.append(Ev)
            self.update_event_dictionaries(Ev)
        # else debug statement I guess

    def add_event(self, event):
        if event.get_num_performances() > 0:
            self.Events.append(event)
            self.update_event_dictionaries(event)

        # else debug statement I guess

    def create_event_list(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                if event.get_num_performances() > 0:
                    self.Events.append(event)
                    self.update_event_dictionaries(event)

    def create_event_list_json(self, events):
        if len(self.Events) > 0:
            print("EventList already contains events")
        else:
            for event in events:
                Ev = Event.Event(event)
                if Ev.get_num_performances() > 0:
                    self.Events.append(Event.Event(event))
                    self.update_event_dictionaries(Event.Event(event))

    def get_events_by_metro_id(self, metro_id):
        return_events = []
        for event in self.Events:
            if event.get_metro_id() == metro_id:
                return_events.append(event)
        return return_events

    def get_events_by_city(self, city):
        return_events = []
        for event in self.Events:
            if event.get_city().lower() == city.lower():
                return_events.append(event)
        return return_events

    def get_events_by_artist(self, artist):
        return_events = []
        for event in self.Events:
            if event.get_artists().lower() == artist.lower():
                return_events.append(event)
        return return_events

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
        temp_event_list = []
        for x in self.Events:
            if x not in temp_event_list:
                temp_event_list.append(x)
        self.reset_event_dict()
        self.Events = temp_event_list

    def get_event_by_id(self, id):
        for event in self.Events:
            if event.get_event_id() == id:
                return event
        return False

    def order_event_list_by_date(self):
        date_id_dict = {}
        temp_event_list = []
        for event in self.Events:
            temp_event_id = event.get_event_id()
            temp_date = event.get_date()
            date_id_dict[temp_event_id] = temp_date
        sorted_dates = dict(
            sorted(date_id_dict.items(), key=lambda item: item[1]))
        for id in sorted_dates.keys():
            temp_event_list.append(self.get_event_by_id(id))
        self.Events = temp_event_list
        self.reset_event_dict()

    def get_events(self):
        return self.Events

    def get_event_dictionaries(self):
        return self.event_dictionaries

    def get_events_in_time_window(self, start_date, end_date):
        temp_event_list = []
        for event in self.Events:
            temp_date = event.get_date()
            if temp_date < end_date and temp_date > start_date:
                temp_event_list.append(event)
        return temp_event_list
