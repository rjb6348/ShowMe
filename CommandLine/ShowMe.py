import Event
import SongKickAPI
import pandas as pd
import ShowMeUtilities as smUtil
import EventList

def main():
    ml = None
    location = None

    searchType = smUtil.promptForSearchType()
    if searchType == False:
        print("Crash Here")
    ml = None
    sk = SongKickAPI.SongKickAPI()

    if searchType == 4 or searchType == 2:
        ml = smUtil.setupML(searchType)
        if ml == False:
            print("Fail")

    location = smUtil.checkToQueryLocation(searchType, sk)

    input = smUtil.createSearchTypeQuery(searchType)

    events = search(searchType, input, location, sk, ml)

    displayEvents = (events, input)


def search(searchType, input, location, sk, ml):
    if searchType == 1:
        events = ArtistSearch(input, location, sk)
    elif searchType == 2:
        events = GenreSearch(input, location, sk, ml)
    elif searchType == 3:
        events = LocationSearch(input, location, sk)
    elif searchType == 4:
        events = LibrarySearch(input, location, sk, ml)

    return events




def ArtistSearch(input, location, sk):
    [artistSearchStatus, artistId] = sk.findArtist(input)
    if artistSearchStatus.lower() == "success":
        EL = EventList.EventList()
        [findArtistEventsStatus, events] = sk.findArtistEvents(input, artistId)
        if findArtistEventsStatus.lower() == "success":
            for event in events:
                EO = Event.Event(event)
                EO.setSearchedArtist(input)
                EL.addEvent(EO)
        if location[1] is not False:
            locEL = EventList.EventList()
            locEL.createEventList(EL.getEventsByMetroId(location[1]))
            locEL.printEvents()
        else:
            EL.printEvents()
        #for event in eventList:
        #    if event != "Failure":
        #        print(input + " is coming to " + event.getCity() + " on " + event.getDate() + " at the " + event.getVenueName())
    else:
        print(artistId)


def GenreSearch(input, ml):
    print("Genre Search")

def LocationSearch(input, location, sk):
    print("Location Search")
    [findArtistEventsStatus, events] = sk.findLocationEvents(location[0][0], location[1])
    if findArtistEventsStatus == "Success":
        EL = EventList.EventList()
        for event in events:
            EL.addEventJson(event)
    EL.printEvents()
    #for event in eventList:
    #    if event != "Failure":
    #        print(event.getHeadliner() + " is coming to " + event.getCity() + " on " + event.getDate() + " at the " + event.getVenueName())

        #df.loc[rank,'status'] = findArtistEventsStatus
        #df.loc[rank,'statusCode'] = events
        

def LibrarySearch(input, location, sk, ml):
    print("Library Search")
    locationId = location[1]
    City = location[0][0]
    if input[0] == 1:
        timeRange = ["long_term"]
    elif input[0] == 2:
        timeRange = ["medium_term"]
    elif input[0] == 3:
        timeRange = ["long_term"]
    elif input[0] == 4:
        timeRange = ["long_term","medium_term","short_term"]

    topArtists = [[] for i in timeRange]
    topArtistStatus = [[] for i in timeRange]
    artistIds, artistNames, artistEvents, status, statusCode = [], [], [], [], []
    print("Pulling Artists")
    for tr in range(0,len(timeRange)):
        [topArtists[tr], topArtistStatus[tr]] = ml.pullUserTopArtists(limit=50, time_range=timeRange[tr])

    for tr in range(0,len(topArtistStatus)):
        if topArtistStatus[tr].lower() == 'success':
            print("Your Top artist of: " + timeRange[tr])
            for i, item in enumerate(topArtists[tr]['items']):
                artistNames.append(item['name'])
                print("Rank " + str(i + 1) + " " + item['name'])
            print()
    artistNames = set(artistNames)
    artistNames = list(artistNames)
    if len(artistNames) > 0:
        artistInfo = {'artistName':artistNames}
        df = pd.DataFrame(data = artistInfo)
    else:
        print("Bad")

    print("Finding Artist Info")
    for artist in artistNames:
        [artistSearchStatus, artistId] = sk.findArtist(artist)
        if artistSearchStatus == "Success":
            artistIds.append(artistId)
            statusCode.append(None)
        else:
            artistIds.append(None)
            statusCode.append(artistId)
        status.append(artistSearchStatus)

    df['status'] = status
    df['statusCode'] = statusCode

    df['artistId'] = artistIds
    print("Finding Artist Events")
    EL = EventList.EventList()

    for rank, [artist, currStatus, currCode, artistId] in df.iterrows():
        if currStatus == "Success":
            eventList = []
            [findArtistEventsStatus, events] = sk.findArtistEvents(artist, artistId)
            if findArtistEventsStatus == "Success":
                for event in events:
                    EO = Event.Event(event)
                    EO.setSearchedArtist(artist)
                    eventList.append(EO)
                    EL.addEventJson(event)
            else:
                eventList.append(status)
                df.loc[rank,'status'] = findArtistEventsStatus
                df.loc[rank,'statusCode'] = events
            artistEvents.append(eventList)
        else:
            artistEvents.append(None)

    if locationId is not False:
        locEL = EventList.EventList()
        locEL.createEventList(EL.getEventsByMetroId(locationId))
        EL = locEL
    #print("Unordered and uncleaned")
    #EL.printEvents()
    EL.cleanEventList()
    #print("Unordered")
    #EL.printEvents()
    EL.orderEventListByDate()
    print("Ordered and sanitized")
    EL.printEvents()

'''
    df['EventList'] = artistEvents
    EventsInCity = []
    for rank, [artist, status, FailureReason, artistId, EventList] in df.iterrows():
        EventsInCityTemp = []
        if status == "Success":
            for event in EventList:
                if event.getMetroId() == locationId:
                    print(artist + " coming to " + event.getCity() + " on " + event.getDate() + " at the " + event.getVenueName())
                    EventsInCityTemp.append(event)
            if len(EventsInCityTemp)==0:
                    EventsInCityTemp.append(None)
                    print(artist + " is touring, but not coming to " + City)
        else:
            print( FailureReason)
            EventsInCityTemp.append(None)
        EventsInCity.append(EventsInCityTemp)

    df['EventsInCity'] = EventsInCity

    print("\n\n\n")
    print("Artist Coming to Metro Area of " + City)
    
    for rank, [artist, status, FailureReason, artistId, EventList, EventsInCity] in df.iterrows():
        if len(EventsInCity) > 0 and EventsInCity[0] is not None:
            for event in EventsInCity:
                print(artist + " coming to " + event.getCity() + " on " + event.getDate() + " at the " + event.getVenueName())
'''


if __name__ == "__main__":
    main()