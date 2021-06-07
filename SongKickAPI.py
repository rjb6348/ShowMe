import requests
import Utilities
#import config

SongkickAPIKey = "P7B3qCrsibrSAPhg"

class SongKickAPI(object):
    key = None
    Base_Search_URL = 'https://api.songkick.com/api/3.0/search/artists.json?query={}&apikey={}'

    def __init__(self, key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = SongkickAPIKey
        self.Base_Artist_Search_URL     = 'https://api.songkick.com/api/3.0/search/artists.json?query={}&apikey={}'
        self.Base_Artist_Event_Search_URL      = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.Base_Location_Search_URL   = 'https://api.songkick.com/api/3.0/search/locations.json?query={}&apikey={}'

    def findArtist(self, ArtistIn):
        artistMatch = False
        Search_Artist_URL= self.Base_Search_URL.format('"'+ArtistIn+'"', SongkickAPIKey)
        r = requests.get(Search_Artist_URL)
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            [status, result] = Utilities.parseSearchResultsArtist(data, ArtistIn)
            if status=="Success":
                return result
            elif status == "Failure":
                print(result)
                return("Status: Fail")
                #return result
            else:
                print("Unhandled Result Status")
            '''
            resultsPage = data["resultsPage"]
            totalResults = resultsPage['totalEntries']
            if totalResults<1:
                print('Artist Not Found')
            elif totalResults==1:
                return resultsPage["results"]["artist"]["id"]
            else:
                results = resultsPage["results"]
                artists = results["artist"]
                #Ask For User Input?
                for artist in artists:
                    if artist["displayName"].lower() == ArtistIn.lower():
                        artistMatch = 1
                        id = artist["id"]
                        return id
                if not artistMatch:
                    print("Artist " + ArtistIn + " Not Found")
                    return False
            '''
        else:
            print("Request Failed")
            return False

    def findCity(self, City, State):#Country=None, State=None, City=None, Venue=None):
        r = requests.get(self.Base_Location_Search_URL.format(City, SongkickAPIKey))
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            [status, result] = Utilities.parseSearchResultsLocationCity(data, City, State)
            if status=="Success":
                return result
            elif status == "Failure":
                print(result)
                return("Status: Fail")
                #return result
            else:
                print("Unhandled Result Status")
        else:
            print("Service Down")


            '''
            results = data['resultsPage']['results']
            locationlist = results['location']
            cityList = []
            stateList = []
            if City:
                for location in locationlist:
                    if location['city']['displayName'].lower() == LocationString.lower():
                        cityList.append(location['metroArea']['id'])
            elif State:
                for location in locationlist:
                    if location['state']['displayName'].lower() == State.lower():
                        stateList.append(location['metroArea']['id'])
            else:
                print("Error, needed City or State Selected")
            '''


    def findArtistEvents(self, Artist=None, ArtistID=None, SearchLocation=None, SearchLocationID=None):
        Search_Event_URL = self.Base_Artist_Event_Search_URL.format(Artist, SongkickAPIKey)
        r = requests.get(Search_Event_URL)
        valid_request = r.status_code in range(200,299)
        ConcertFound = False
        locations = []
        if valid_request:
            data = r.json()
            results = data['resultsPage']['results']
            eventlist = results['event']
            for event in eventlist:
                locations.append(event['location']['city'])
            if SearchLocation:
                for location in locations:
                    if SearchLocation in location:
                        print(location)
        else:
            print("Service Down")
                
        #
        #if 'NJ' in location:
        #    print("NJ Found")
    """
        if "Camden" in event['location']['city'].split(',')[0]:
            #.split(',')[0]:
            print("Good News!")
            print(ArtistName + " is coming to philadelphia! on " + event['start']['date'])
            ConcertFound = True
    if not ConcertFound:
        for event in eventlist:
            if "NJ" in event['location']['city']:
                print("Coming to " + event['location'] + " on: " + event['start']['date'])
    """


        
    #if not ConcertFound:
    #    print("No luck Finding any shows for " + ArtistName)

#print(r)