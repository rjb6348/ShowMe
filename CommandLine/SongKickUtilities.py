def parseSearchResultsLocationCity(data, cityString, stateString):

    resultsPage = data["resultsPage"]
    totalResults = resultsPage['totalEntries']
    if totalResults<1:
        print('No City Found matching description: ' + cityString)
        return ["Failure", 'No City Found matching description: ' + cityString]
    else:
        results = data['resultsPage']['results']
        locationlist = results['location']
        cityList = []
        matchingCityind = []
        citStateList = []
        if totalResults == 1:
            if 'state' in locationlist[0]['city'].keys():
                if locationlist[0]['city']['state']['displayName'].lower() == stateString.lower():
                    return ["Success",locationlist[0]['metroArea']['id']]
                else:
                    return ["Failure","City in wrong State"]
            else:
                return ["Failure","Matching City not in US"]
        else:
            for i in range(0,len(locationlist)):
                if locationlist[i]['city']['displayName'].lower() == cityString.lower():
                    cityList.append(locationlist[i]['metroArea']['id'])
                    matchingCityind.append(i)
            for i in range(0,len(matchingCityind)):
                if 'state' in locationlist[i]['city'].keys():
                    if locationlist[i]['city']['state']['displayName'].lower() == stateString.lower():
                        citStateList.append(locationlist[i]['metroArea']['id'])
            if len(cityList)==0:
                print("Error, City entered and ")
                return ["Failure", 'A Location that is not a city found for: ' + cityString]
            elif len(cityList)==1:
                return ["Success", cityList[0]]
            else:
                if len(citStateList) == 0:
                    return ["Failure", "City Exists, but not in provided State"]
                elif len(citStateList) == 1:
                    return ["Success", citStateList[0]]
                else:
                    return ["Failure", "Multiple Cities exist with Name x in State y"]

def parseSearchResultsArtist(data, searchString):
    resultsPage = data["resultsPage"]
    totalResults = resultsPage['totalEntries']
    if totalResults<1:
        return ["Failure", 'No Artist Found matching description: ' + searchString]
    elif totalResults==1:
        return ["Success",resultsPage["results"]["artist"][0]["id"]]
    else:
        results = resultsPage["results"]
        artists = results["artist"]
        artistList = []
        #Ask For User Input?
        for artist in artists:
            if artist["displayName"].lower() == searchString.lower():
                artistList.append(artist["id"])

        if artistList is None or len(artistList)==0:
            print("Artist " + searchString + " Not Specific Enough")
            return [False, "No Matching Artists: " + searchString + " Not Specific Enough"]
        elif len(artistList)==1:
            return ["Success", artistList[0]]
        else:
            print("Too Many Matching Artists: " + searchString + " Not Specific Enough")
            return [False, "Too Many Matching Artists: " + searchString + " Not Specific Enough"]
