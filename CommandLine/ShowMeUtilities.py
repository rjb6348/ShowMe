from pyzipcode import ZipCodeDatabase
import MusicLibrary

def setupML(searchType):
    print("Time to Login to Spotify!")
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'
    loggedIn = False
    try:
        ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
        while loggedIn == False:
            username = input("What's your username: ")
            loginStatus = ml.login(username)
            if loginStatus.lower() != "success":
                print("Login Failed.")
                again = input("Try again (y/n): ")
                if again == 'n':
                    break
            else:
                loggedIn = True
        return ml
    except:
        print("Login Failed Unexpectedly")
        return False

def promptForSearchTypeOld():
    #Step1: Get User Input
    readyToSearch = False
    while readyToSearch == False:
        print("How do you want to find concerts?")
        print("1: Search by Artist")
        print("2: Search by Location")
        print("3: Search by Music Library")
        searchType = input("Enter Search Type (1-3): ")
        if searchType == None or searchType == "":
            print("Warning: No input selected.")
            again = True
            while again == True:
                againIn = input("Try again (y/n): ")
                if againIn.lower() == 'n':
                    return False
                elif againIn.lower() == 'y':
                    again = False
                else:
                        print("Waning:  Unrecognized input. Only y or n accepted")
                continue
        elif searchType.isnumeric() == False or int(searchType) not in range(1,4):
            print("Warning: Enter an option between 1 and 3")
            again = True
            while again == True:
                againIn = input("Try again (y/n): ")
                if againIn.lower() == 'n':
                    return False
                elif againIn.lower() == 'y':
                    again = False
                else:
                    print("Waning:  Unrecognized input. Only y or n accepted")
                continue
        elif int(searchType) in range(1,4):
            return int(searchType)
        else:
            print("Unrecognized or unhandled input.  Bad Job")
            return False

def createSearchTypeQueryOld(searchType):
    searchQuery = []
    if searchType == 1:
        searchQuery = input("What is the artist/band you want to find a tour for?: ")
    elif searchType == 3:
        while searchQuery == []:
            print("What Period of your listening history do you want to find your Top Artists From?  ")
            print("1: Top Artists from Long Term")
            print("2: Top Artist from Medium Term")
            print("3: Top Artist from Short Term")
            print("4: Top Artists from each period")
            searchPeriod = input("Enter Period Length (1-4): ")
            if searchPeriod == None or searchPeriod == "":
                print("Warning: No input selected.")
                again = True
                while again == True:
                    againIn = input("Try again (y/n): ")
                    if againIn.lower() == 'n':
                        return [False]
                    elif againIn.lower() == 'y':
                        again = False
                    else:
                        print("Waning:  Unrecognized input. Only y or n accepted")
                continue
            elif searchPeriod.isnumeric() == False or int(searchPeriod) not in range(1,5):
                print("Warning: Enter an option between 1 and 4")
                again = True
                while again == True:
                    againIn = input("Try again (y/n): ")
                    if againIn.lower() == 'n':
                        return [False]
                    elif againIn.lower() == 'y':
                        again = False
                    else:
                        print("Waning:  Unrecognized input. Only y or n accepted")
                continue
            elif int(searchPeriod) in range(1,5):
                timeRange = []
                if int(searchPeriod) == 1:
                    timeRange = ["long_term"]
                elif int(searchPeriod) == 2:
                    timeRange = ["medium_term"]
                elif int(searchPeriod) == 3:
                    timeRange = ["long_term"]
                elif int(searchPeriod) == 4:
                    timeRange = ["long_term","medium_term","short_term"]
                searchQuery.append(timeRange)
            else:
                print("Unhandled input.  Bad Job")
                return [False]
    return searchQuery

def checkToQueryLocation(searchType, sk):
    locFound = False
    if searchType != 2:
        again = True
        while again == True:
            citySpecific = input("Do you want to see tours in a specific city? (y/n): ")
            if citySpecific.lower() == "y":
                cityState =  queryLocation()
                again = False
            elif citySpecific.lower() == "n":
                return [[False,False], False]
            else:
                print("Waning:  Unrecognized input. Only y or n accepted")
            continue
    else:
        cityState = queryLocation()
    while locFound == False:
        [locStatus, locId] = sk.findCity(cityState[0],cityState[1])
        if locStatus.lower() == 'success':
            locFound = True
        else:
            print("City, State Combination not found.")
            again = input("Try again? (y/n): ")
            if again:
                cityState = queryLocation()
            else: 
                return False
    return [cityState, locId]

def queryLocation():
    searchQuery = []
    while searchQuery == []:
        print("Do you want to search by: ")
        print("1: City & State")
        print("2: Zip")
        LocType = input("Enter Search Type (1 or 2): ")
        if LocType == None or LocType == "":
            print("Warning: No input selected.")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif LocType.isnumeric() == False or int(LocType) not in range(1,3):
            print("Warning: Enter either a 1 or 2")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif int(LocType) == 1:
            state = input("Enter two letter State Abbreviation (ex: PA): ")
            city = input("Enter the City: ")
            searchQuery = [city, state]
        elif int(LocType) == 2:
            zcdb = ZipCodeDatabase()
            zip = input("Enter Zip Code: ")
            zipcode = zcdb[int(zip)]
            searchQuery =  [zipcode.city, zipcode.state]

        else:
            print("I do not understand how we got here")
        return searchQuery





def queeryDateRange():
    searchQuery = []
    again = True
    while again == True:
        dateFilter = input("Do you want to filter results by Date? (y/n) ")
        if dateFilter.lower() == "y":
            again = False
        elif dateFilter.lower() == "n":
            return False
        else:
            print("Waning:  Unrecognized input. Only y or n accepted")
        continue

    # Date Query

    while searchQuery == []:
        print("Do you want to search by: ")
        print("1: Month")
        print("2: Start Date & End Date")
        dateSearchType = input("Enter Search Type (1 or 2): ")
        if dateSearchType == None or dateSearchType == "":
            print("Warning: No input selected.")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif dateSearchType.isnumeric() == False or int(LocType) not in range(1,3):
            print("Warning: Enter either a 1 or 2")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif int(LocType) == 1:
            state = input("Enter two letter State Abbreviation (ex: PA): ")
            city = input("Enter the City: ")
            searchQuery = [city, state]
        elif int(LocType) == 2:
            zcdb = ZipCodeDatabase()
            zip = input("Enter Zip Code: ")
            zipcode = zcdb[int(zip)]
            searchQuery =  [zipcode.city, zipcode.state]
        else:
            print("I do not understand how we got here")
        return searchQuery


def promptForSearchType():
    results = queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
    return results

def createSearchTypeQuery(searchType):
    searchQuery = []
    if searchType == 1:
        results = input("What is the artist/band you want to find a tour for?: ")
    elif searchType == 3:
        searchQuery = ["Top Artists from Long Term", "Top Artist from Medium Term",
                        "Top Artist from Short Term", "Top Artists from each period"]
        results = queryStandard(searchQuery)
        if int(results) in range(1,5):
            if int(results) == 1:
                results = ["long_term"]
            elif int(results) == 2:
                results = ["medium_term"]
            elif int(results) == 3:
                results = ["long_term"]
            elif int(results) == 4:
                results = ["long_term","medium_term","short_term"]
    return results


def queryStandard(options):
    result = None
    while result == None:
        print("Do you want to search by: ")
        for i in range(1,len(options)+1):
            print(str(i) + ": " + options[i-1])
        inputString = input("")

        if inputString == None or inputString == "":
            print("Warning: No input selected.")
            again = True
            while again == True:
                againIn = input("Try again (y/n): ")
                if againIn.lower() == 'n':
                    return False
                elif againIn.lower() == 'y':
                    again = False
                else:
                    print("Waning:  Unrecognized input. Only y or n accepted")
            continue
        elif inputString.isnumeric() == False or int(inputString) not in range(1, len(options)+1):
            print("Warning: Enter a number betwee 1 and " + str(len(options)))
            again = True
            while again == True:
                againIn = input("Try again (y/n): ")
                if againIn.lower() == 'n':
                    return [False]
                elif againIn.lower() == 'y':
                    again = False
                else:
                    print("Waning:  Unrecognized input. Only y or n accepted")
            continue
        elif int(inputString) in range(1, len(options)+1):
            return int(inputString)
        else:
            print("Unhandled Input")
            return False

