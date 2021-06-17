import requests
import SongKickUtilities
#import config

SongkickAPIKey = "P7B3qCrsibrSAPhg"

class SongKickAPI(object):
 
    def __init__(self, key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = SongkickAPIKey
        self.Base_Artist_Search_URL     = 'https://api.songkick.com/api/3.0/search/artists.json?query={}&apikey={}'
        self.Base_Artist_Event_Search_URL      = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.Base_Location_Search_URL   = 'https://api.songkick.com/api/3.0/search/locations.json?query={}&apikey={}'
        self.Base_Location_Event_Search_URL = 'https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?apikey={}'


    def findArtist(self, ArtistIn):
        Search_Artist_URL= self.Base_Artist_Search_URL.format('"' + ArtistIn + '"', SongkickAPIKey)
        r = requests.get(Search_Artist_URL)
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            [status, returnData] = SongKickUtilities.parseSearchResultsArtist(data, ArtistIn)
        else:
            status = "Failure"
            returnData = "Invalid Request Code: " + r.status_code
        return [status, returnData]

    def findCity(self, City, State):
        r = requests.get(self.Base_Location_Search_URL.format(City, SongkickAPIKey))
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            [status, returnData] = SongKickUtilities.parseSearchResultsLocationCity(data, City, State)
        else:
            status = "Failure"
            returnData = "Invalid Request Code: " + r.status_code
        return [status, returnData]

    def findArtistEvents(self, Artist, ArtistId):
        Search_Event_URL = self.Base_Artist_Event_Search_URL.format(ArtistId, SongkickAPIKey)
        r = requests.get(Search_Event_URL)
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            resultsPage = data['resultsPage']
            totalEntries =  resultsPage["totalEntries"]
            if totalEntries == 0:
                status = "Failure"
                returnData = "The Artist: " + Artist + " is not on tour"
            else:
                results = resultsPage['results']
                returnData = results['event']
                status = "Success"
        else:
            status = "Failure"
            returnData = "Invalid Request Code: " + str(r.status_code)
        return [status, returnData]

    def findLocationEvents(self, Location, LocationId):
        Search_Location_Event_URL = self.Base_Location_Event_Search_URL.format(LocationId, SongkickAPIKey)
        r = requests.get(Search_Location_Event_URL)
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            resultsPage = data['resultsPage']
            totalEntries =  resultsPage["totalEntries"]
            if totalEntries == 0:
                returnData = "The Location: " + Location + " does not have any events"
                status = "Failure"
            else:
                results = resultsPage['results']
                returnData = results['event']
                status = "Success"
        else:
            status = "Failure"
            returnData = "Invalid Request Code: " + r.status_code    
        return [status, returnData]
