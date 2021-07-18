def parse_search_results_location_city(data, city_string, state_string):

    results_page = data["resultsPage"]
    total_results = results_page['totalEntries']
    if total_results < 1:
        print('No City Found matching description: ' + city_string)
        return ["Failure", 'No City Found matching description: ' + city_string]
    else:
        results = data['resultsPage']['results']
        location_list = results['location']
        city_list = []
        matching_city_ind = []
        city_state_list = []
        if total_results == 0:
            return ["Failure", "No Results"]
        elif total_results == 1:
            if 'state' in location_list[0]['city'].keys():
                if location_list[0]['city']['state']['displayName'].lower() == state_string.lower():
                    return ["Success", location_list[0]['metroArea']['id']]
                else:
                    return ["Failure", "City in wrong State"]
            else:
                return ["Failure", "Matching City not in US"]
        else:
            for i in range(0, len(location_list)):
                if location_list[i]['city']['displayName'].lower() == city_string.lower():
                    city_list.append(location_list[i]['metroArea']['id'])
                    matching_city_ind.append(i)
            for i in range(0, len(matching_city_ind)):
                if 'state' in location_list[i]['city'].keys():
                    if location_list[i]['city']['state']['displayName'].lower() == state_string.lower():
                        city_state_list.append(location_list[i]['metroArea']['id'])
            if len(city_list) == 0:
                print("Error, City entered and ")
                return ["Failure", 'A Location that is not a city found for: ' + city_string]
            elif len(city_list) == 1:
                return ["Success", city_list[0]]
            else:
                if len(city_state_list) == 0:
                    return ["Failure", "City Exists, but not in provided State"]
                elif len(city_state_list) == 1:
                    return ["Success", city_state_list[0]]
                else:
                    return ["Failure", "Multiple Cities exist with Name x in State y"]


def parse_search_results_artist(data, search_string):
    results_page = data["resultsPage"]
    total_results = results_page['totalEntries']
    if total_results < 1:
        return ["Failure", 'No Artist Found matching description: ' + search_string]
    elif total_results == 1:
        return ["Success", results_page["results"]["artist"][0]]
    else:
        results = results_page["results"]
        artists = results["artist"]
        artist_list = []
        # Ask For User Input?
        for artist in artists:
            if artist["displayName"].lower() == search_string.lower():
                artist_list.append(artist)

        if artist_list is None or len(artist_list) == 0:
            print("Artist " + search_string + " Not Specific Enough")
            return [False, "No Matching Artists: " + search_string + " Not Specific Enough"]
        elif len(artist_list) == 1:
            return ["Success", artist_list[0]]
        else:
            print("Too Many Matching Artists: " +
                  search_string + " Not Specific Enough")
            return [False, "Too Many Matching Artists: " + search_string + " Not Specific Enough"]
