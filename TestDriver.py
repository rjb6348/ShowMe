import MusicLibrary
import SongKickAPI
import pandas as pd
import Event
#from pandas import dataframe as df
def testSpotify():
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'

    ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)

    login_status = ml.login('rrbvt')
    check_status("Login", login_status)

    ml.dispUser()

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10)
    check_status("Pull Tracks", TopArtist_status)
    print("Long_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10,time_range="medium_term")
    check_status("Pull Tracks", TopArtist_status)
    print("Medium_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10,time_range="short_term")
    check_status("Pull Tracks", TopArtist_status)
    print("Short_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 


def testSongKickApi():
    sk = SongKickAPI.SongKickAPI()
    artist = 'The Killers'
    [status, artistId] = sk.findArtist(artist)
    #print(artistId)
    [status, LocationId] = sk.findCity('Philadelphia','PA')
    #print(LocationId)
    [status, Events] = sk.findArtistEvents(ArtistId = artistId, Artist = artist)
    #print(Events)

def testCombo():
    #Variable Setup
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'
    artistIds, artistNames, artistEvents, status, statusCode = [],[],[],[],[]

    #initialize services classes
    ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
    sk = SongKickAPI.SongKickAPI()

    City = 'Philadelphia'
    State = 'PA'

    [locationStatus, locationId] = sk.findCity(City,State)
    if locationStatus == "Failure":
        raise Exception("Location not found")

    login_status = ml.login('rrbvt')
    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=100)
    print("Long_Term")
    print("Number\tArtist")

    for i, item in enumerate(TopArtists['items']):
        artistNames.append(item['name'])
    artistInfo = {'artistName':artistNames}
    df = pd.DataFrame(data = artistInfo)

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
    for rank, [artist, currStatus, currCode, artistId] in df.iterrows():
            if currStatus == "Success":
                eventList = []
                [findArtistEventsStatus, events] = sk.findArtistEvents(artist, artistId)
                if findArtistEventsStatus == "Success":
                    for event in events:
                        eventList.append(Event.Event(event))
                else:
                    eventList.append(status)
                    df.loc[rank,'status'] = findArtistEventsStatus
                    df.loc[rank,'statusCode'] = events

                artistEvents.append(eventList)
            else:
                artistEvents.append(None)


    df['EventList'] = artistEvents
    EventsInCity = []
    for rank, [artist, status, FailureReason, artistId, EventList] in df.iterrows():
        EventsInCityTemp = []
        if status == "Success":
            for event in EventList:
                if event.getMetroId() == locationId:
                    print(artist + " coming to " + event.getLocation() + " on " + event.getDate() + " at the " + event.getVenueName())
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
                print(artist + " coming to " + event.getLocation() + " on " + event.getDate() + " at the " + event.getVenueName())



'''
            if artistId is not None:
                for event in EventList:
                    if event is not "Failure":
                        if event.getMetroId() == locationId:
                            print(artist + " coming to " + event.getLocation() + " on " + event.getDate() + " at the " + event.getVenueName())
                    else:
                        print(artist + " "+ event[1])
                eventList = []
                [status, events] = sk.findArtistEvents(artist, artistId)
                if status == "Success":
                    for event in events:
                        eventList.append(Event.Event(event))
                else:
                    eventList.append(status)
                artistEvents.append(eventList)

'''
'''    
    for i in range(0,len(eventList[0])):
        print(eventList[i] + "    " + eventList[i])
    print("    ")
'''

def check_status(step, return_status):
    if return_status.lower() == "success":
        return
    elif return_status.lower() == "warning":
        return
    elif return_status.lower() == "error":
        raise Exception(["Step: " + step + " Errored"])
    else:
        Exception(["Unhandled Return Status: " + return_status])

if __name__ == "__main__":
    testSpotify()
    testSongKickApi()
    testCombo()
