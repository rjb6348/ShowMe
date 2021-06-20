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

    if searchType == 3:
        ml = smUtil.setupML(searchType)
        if ml == False:
            print("Fail")

    location = smUtil.checkToQueryLocation(searchType, sk)

    dateRange = smUtil.queeryDateRange()

    input = smUtil.createSearchTypeQuery(searchType)

    events = search(searchType, input, location, sk, ml, dateRange)

    #displayEvents = (events, input)


def search(searchType, input, location, sk, ml, dateRange):
    if searchType == 1:
        events = ArtistSearch(input, location, sk, dateRange)
    elif searchType == 2:
        events = LocationSearch(input, location, sk, dateRange)
    elif searchType == 3:
        events = LibrarySearch(input, location, sk, ml, dateRange)
    return events




def ArtistSearch(input, location, sk, dateRange):
    [artistSearchStatus, artistId] = sk.findArtist(input)
    if dateRange[0] == False:
        dr=None
    else:
        dr = dateRange
    if location[1] == False:
        loc = None
    else:
        loc = location[1]

    if artistSearchStatus.lower() == "success":
        EL = EventList.EventList()
        [findArtistEventsStatus, events] = sk.findArtistEvents(input, artistId, dateRange=dr, metroId=loc)
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
    else:
        print(artistId)

def LocationSearch(input, location, sk, dateRange):
    print("Location Search")
    if dateRange[0] == False:
        dr=None
    else:
        dr = dateRange
    [findArtistEventsStatus, events] = sk.findLocationEvents(location[0][0], location[1], dateRange=dr)
    EL = EventList.EventList()
    if findArtistEventsStatus == "Success":
        for event in events:
            EL.addEventJson(event)
    EL.printEvents()
        

def LibrarySearch(input, location, sk, ml, dateRange):
    print("Library Search")
    locationId = location[1]
    City = location[0][0]
    timeRange = input
    if dateRange[0] == False:
        dr=None
    else:
        dr = dateRange
    if location[1] == False:
        loc = None
    else:
        loc = location[1]
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
            [findArtistEventsStatus, events] = sk.findArtistEvents(artist, artistId, dateRange=dr, metroId=loc)
            if findArtistEventsStatus == "Success":
                for event in events:
                    EO = Event.Event(event)
                    EO.setSearchedArtist(artist)
                    eventList.append(EO)
                    EL.addEvent(EO)
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

if __name__ == "__main__":
    main()