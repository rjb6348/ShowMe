from pyzipcode import ZipCodeDatabase
import MusicLibrary
import datetime
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

def checkToQueryLocation(searchType, sk):
    locFound = False
    if searchType != 2:
        again = True
        while again == True:
            citySpecific = input("Do you want to see tours in a specific city? (y/n): ")
            if citySpecific.lower() == "y":
                cityState =  queryLocation()
                if cityState == [False,False]:
                    return [[False,False], False]
                again = False
            elif citySpecific.lower() == "n":
                return [[False,False], False]
            else:
                print("Waning:  Unrecognized input. Only y or n accepted")
    else:
        cityState = queryLocation()
        if cityState == [False,False]:
            return [[False,False], False]
    while locFound == False:
        [locStatus, locId] = sk.findCity(cityState[0],cityState[1])
        if locStatus.lower() == 'success':
            locFound = True
        else:
            print("City, State Combination not found.")
            again = againQuery()
            if again:
                cityState = queryLocation()
            else: 
                return False
    return [cityState, locId]

def queryLocation():
    results = queryStandard(["City & State", "Zip"])
    if results == False:
        searchQuery = [False, False]
    elif results == 1:
        #validLoc = False TODO: Add location validation here
        #while validLoc == False:
        state = input("Enter two letter State Abbreviation (ex: PA): ")
        city = input("Enter the City: ")
        #    validLoc = validateLoc(city, state)
        searchQuery = [city, state]
    elif results == 2:
        zcdb = ZipCodeDatabase()
        zipFound = False
        while zipFound == False:
            try:
                zip = input("Enter Zip Code: ")
                zipcode = zcdb[int(zip)]
                zipFound = True
            except:
                print("Zip " + zip + " not found.")
                again = againQuery()
                if again:
                    continue
                else:
                    return [False, False]
        searchQuery =  [zipcode.city, zipcode.state]
    else:
        print("I do not understand how we got here")
        searchQuery = [False, False]
    return searchQuery

def queeryDateRange():
    again = True
    while again == True:
        dateFilter = input("Do you want to search results by Date? (y/n) ")
        if dateFilter.lower() == "y":
            again = False
        elif dateFilter.lower() == "n":
            return [False, False]
        else:
            print("Waning:  Unrecognized input. Only y or n accepted")
    startDateGood = False
    while startDateGood == False:
        print('What date do you want to start searching from? (mm/dd/yyyy)')
        startDate = input("Start Date: ")
        try:
            month1, day1, year1 = startDate.split('/')
            date1 = datetime.datetime(int(year1),int(month1),int(day1))
            if date1 < datetime.datetime.combine(datetime.date.today(), datetime.time(0,0)):
                print("Warning: Start date needs to be after today")
            else:
                startDateGood = True
        except ValueError:
            print("Warning: Start Date " + startDate + " not in correct format (mm/dd/yyyy)")
    endDateGood = False
    while endDateGood == False:
        print('What date do you want to stop searching from? (mm/dd/yyyy)')
        endDate = input("Stop Date: ")
        try:
            month2, day2, year2 = endDate.split('/')
            date2 = datetime.datetime(int(year2),int(month2),int(day2))
            if date2>date1:
                endDateGood = True
                startDate = "-".join([year1,month1,day1])
                endDate = "-".join([year2,month2,day2])
            else:
                print("Warning: End date has to be after start date of: " + str(date1))
        except ValueError:
            print("Warning: End Date " + endDate + " not in correct format (mm/dd/yyyy)")

    return [startDate, endDate]

def promptForSearchType():
    results = queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
    return results

def createSearchTypeQuery(searchType):
    searchQuery = []
    results = []
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

def againQuery():
    again = True
    while again == True:
        againIn = input("Try again (y/n): ")
        if againIn.lower() == 'n':
            return False
        elif againIn.lower() == 'y':
            return True
        else:
            print("Waning:  Unrecognized input. Only y or n accepted")

def queryStandard(options):
    result = None
    while result == None:
        print("Do you want to search by: ")
        for i in range(1,len(options)+1):
            print(str(i) + ": " + options[i-1])
        inputString = input("Search By: ")

        if inputString == None or inputString == "":
            print("Warning: No input selected.")
            again = againQuery()
            if again:
                continue
            else:
                return False
        elif inputString.isnumeric() == False or int(inputString) not in range(1, len(options)+1):
            print("Warning: Enter a number betwee 1 and " + str(len(options)))
            again = againQuery()
            if again:
                continue
            else:
                return False
        elif int(inputString) in range(1, len(options)+1):
            return int(inputString)
        else:
            print("Unhandled Input")
            return False
