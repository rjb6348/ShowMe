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
            return ["Success",locationlist['metroArea']['id']]
        else:
            for i in range(0,len(locationlist)):
                if locationlist[i]['city']['displayName'].lower() == cityString.lower():
                    cityList.append(locationlist[i]['metroArea']['id'])
                    matchingCityind.append(i)
            for i in range(0,len(matchingCityind)):
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
                    return ["Success", cityList[0]]
                else:
                    return ["Failure", "Multiple Cities exist with Name x in State y"]

def parseSearchResultsArtist(data, searchString):
    resultsPage = data["resultsPage"]
    totalResults = resultsPage['totalEntries']
    if totalResults<1:
        print('Artist Not Found')
    elif totalResults==1:
        return resultsPage["results"]["artist"]["id"]
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



'''
NOTE: DEAD ATTEMPTED CODE.  KEEPING FOR LATER ABSTRACTION
Not yet supported
def parseSearchResultsLocationState(data, searchString):
    results = data['resultsPage']['results']
    locationlist = results['location']
    cityList = []
    stateList = []
    if ResultsType=="City":
        for location in locationlist:
            if location['city']['displayName'].lower() == searchString.lower():
                cityList.append(location['metroArea']['id'])
    elif ResultsType="State":
        for location in locationlist:
            if location['state']['displayName'].lower() == searchString.lower():
                stateList.append(location['metroArea']['id'])
    else:
        print("Error, needed City or State Selected")
def findKey(key, d, path=[], found=False):

    for k, v in d.items():
        if isinstance(v,list):
            for i in v:
                if isinstance(i,dict):
                    path.append(k)
                    [found,path] = findKey(key,i,path)
                    if found:
                        return [found,path]
                    else:
                        path.pop()
                        return [False, path]
        if found:
            return [True, path]
        if key.lower() == k.lower():
            found = True
            return [found, path]
        elif isinstance(v, dict):
            path.append(k)
            [found,path] = findKey(key,v,path)
            if found:
                return [found,path]
            else:
                return [False, path]
    if len(path)>0:
        path.pop()
        return [False, path]
def parseSearchResults(data, searchString, ResultsType):
    KeyStrings = None
    if ResultsType == "Artist":
        KeyStrings = "artist"
    elif ResultsType == "City" or ResultsType == "State":
        KeyStrings = "location"
    else:
        return(["Fail","Unsupported Results Type"])

    resultsPage = data["resultsPage"]
    totalResults = resultsPage['totalEntries']

    if totalResults < 1:
        print(ResultsType + ' Not Found')
        return(["Fail", ResultsType + " Not Found"])
    else:
        [foundkey, path] = findKey(ResultsType.lower(), resultsPage)
        if not foundkey:
            print("Key " + ResultsType + " Not Found in dict")
            return(["Fail","Unsupported Search Term"])
        if totalResults == 1:
            id = []
            results = resultsPage
            for key in range(0,len(path)-1):
                results = results[path[key]]
            return results["id"]

            #results = resultsPage["results"][KeyStrings]

            #if "displayName" in results.keys():
            #    return ["Success", results["id"]]
            #elif ResultsType.lower() in results.key():
            #        results[ResultsType.lower()]["displayName"]
        else:
            results = resultsPage
            for key in path:
                results = results[key]
            resultList = results
            matchListName = []
            matchListId = []
            if isinstance(resultList, list):
                if isinstance(resultList[0], dict):
                    namePath = findKey('displayPath', resultList[0])
            for result in resultList:
                if isinstance(result, dict):
                    name = result
                    for key in namePath:
                        name = name[key]
                if name.lower() == searchString.lower():
                    id = result
                    for i in range(namePath)-1:
                        id = id[key(i-1)]
                    return id["id"]
            if len(matchListId):
                return(["Success", matchListId[0]])
            else:
                print("Search String Not Specific Enough")
                #Will have page to have user select from results/images
                return(["Fail", "Too Many Results.  Not yet supported"])


def findKey(key, d, path=[], found=False):

    for k, v in d.items():
        if isinstance(v,list):
            for i in v:
                if isinstance(i,dict):
                    path.append(k)
                    [found,path] = findKey(key,i,path)
                    if found:
                        return [found,path]
                    else:
                        path.pop()
                        return [False, path]
        if found:
            return [True, path]
        if key.lower() == k.lower():
            found = True
            return [found, path]
        elif isinstance(v, dict):
            path.append(k)
            [found,path] = findKey(key,v,path)
            if found:
                return [found,path]
            else:
                return [False, path]
    if len(path)>0:
        path.pop()
        return [False, path]
'''