import requests
import SongKickUtilities
#import config

songkick_api_key = "P7B3qCrsibrSAPhg"


class SongKickAPI(object):

    def __init__(self, key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = songkick_api_key
        self.base_artist_search_url = 'https://api.songkick.com/api/3.0/search/artists.json?query={}&apikey={}'
        self.base_artist_event_search_url = "https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}"
        self.base_location_search_url = 'https://api.songkick.com/api/3.0/search/locations.json?query={}&apikey={}'
        self.base_location_event_search_url = 'https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?apikey={}'

    def find_artist(self, artist_in):
        search_artist_url = self.base_artist_search_url.format(
            '"' + artist_in + '"', songkick_api_key)
        r = requests.get(search_artist_url)
        valid_request = r.status_code in range(200, 299)
        if valid_request:
            data = r.json()
            [status, return_data] = SongKickUtilities.parse_search_results_artist(
                data, artist_in)
        else:
            status = "Failure"
            return_data = "Invalid Request Code: " + r.status_code
        return [status, return_data]

    def find_city(self, city, state):
        r = requests.get(
            self.base_location_search_url.format(city, songkick_api_key))
        valid_request = r.status_code in range(200, 299)
        if valid_request:
            data = r.json()
            [status, return_data] = SongKickUtilities.parse_search_results_location_city(
                data, city, state)
        else:
            status = "Failure"
            return_data = "Invalid Request Code: " + r.status_code
        return [status, return_data]

    def find_artist_events(self, artist, artist_id, date_range=None, metro_id=None):
        search_event_url = self.base_artist_event_search_url.format(
            artist_id, songkick_api_key)
        additions = ""
        if date_range is not None:
            min_date = date_range[0]
            max_date = date_range[1]
            additions = additions + "&min_date=" + \
                str(min_date) + "&max_date=" + str(max_date)
        if metro_id is not None:
            additions = additions + "&metro_area_id=" + str(metro_id)

        search_event_url = search_event_url + additions
        r = requests.get(search_event_url)
        valid_request = r.status_code in range(200, 299)
        if valid_request:
            data = r.json()
            results_page = data['resultsPage']
            total_entries = results_page["totalEntries"]
            if total_entries == 0:
                status = "Failure"
                return_data = "The Artist: " + artist + " is not on tour"
            else:
                results = results_page['results']
                return_data = results['event']
                status = "Success"
        else:
            status = "Failure"
            return_data = "Invalid Request Code: " + str(r.status_code)
        return [status, return_data]

    def find_location_events(self, location, location_id, date_range=None):
        search_location_event_url = self.base_location_event_search_url.format(
            location_id, songkick_api_key)
        additions = ""
        if date_range is not None:
            min_date = date_range[0]
            max_date = date_range[1]
            additions = additions + "&min_date=" + \
                str(min_date) + "&max_date=" + str(max_date)
        search_location_event_url = search_location_event_url + additions
        r = requests.get(search_location_event_url)
        valid_request = r.status_code in range(200, 299)
        if valid_request:
            data = r.json()
            results_page = data['resultsPage']
            total_entries = results_page["totalEntries"]
            if total_entries == 0:
                return_data = "The Location: " + location + " does not have any events"
                status = "Failure"
            else:
                results = results_page['results']
                return_data = results['event']
                status = "Success"
        else:
            status = "Failure"
            return_data = "Invalid Request Code: " + r.status_code
        return [status, return_data]
