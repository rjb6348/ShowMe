from pyzipcode import ZipCodeDatabase
import MusicLibrary

def setupML(searchType):
    print("Time to Login to Spotify!")
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'
    loggedIn = False
    if searchType == 4:
        try:
            ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
            while loggedIn == False:
                username = input("What's your username: ")
                if ml.dispUser() != username:
                    ml.logout()
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
    elif searchType == 2:
        print("No login needed")

def promptForSearchType():
    #Step1: Get User Input
    readyToSearch = False
    while readyToSearch == False:
        print("How do you want to find concerts?")
        print("1: Search by Artist")
        print("2: Search by Genre")
        print("3: Search by Location")
        print("4: Search by Music Library")
        searchType = input("Enter Search Type (1-4): ")
        if searchType == None or searchType == "":
            print("Warning: No input selected.")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif searchType.isnumeric() == False or int(searchType) not in range(1,5):
            print("Warning: Enter an option between 1 and 4")
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif int(searchType) == 2:
            print("Warning: Genre Search not yet supported. Select another") #TODO figure out where to get top artists per genre from???
            again = input("Try again (y/n): ")
            if again == 'n':
                return False
            else:
                continue
        elif int(searchType) in range(1,5):
            return int(searchType)
        else:
            print("Unrecognized or unhandled input.  Bad Job")
            return False

def createSearchTypeQuery(searchType):
    searchQuery = []
    if searchType == 1:
        searchQuery = input("What is the artist/band you want to find a tour for?: ")
    elif searchType == 2:
        searchQuery = input("Which genre do you want to search for?: ")
    elif searchType == 4:
        while searchQuery == []:
            print("What Period of your listening history do you want to find your Top Artists From?  ")
            print("1: Top Artists from Long Term")
            print("2: Top Artist from Medium Term")
            print("3: Top Artist from Short Term")
            print("4: Top Artists from each period")
            searchPeriod = input("Enter Period Length (1-4): ")
            if searchPeriod == None or searchPeriod == "":
                print("Warning: No input selected.")
                again = input("Try again (y/n): ")
                if again == 'n':
                    return False
                else:
                    continue
            elif searchPeriod.isnumeric() == False or int(searchPeriod) not in range(1,5):
                print("Warning: Enter an option between 1-4")
                again = input("Try again (y/n): ")
                if again == 'n':
                    return False
                else:
                    continue
            elif int(searchPeriod) in range(1,5):
                searchQuery.append(int(searchPeriod))
            else:
                print("Unrecognized or unhandled input.  Bad Job")
                return False
    return searchQuery

def checkToQueryLocation(searchType, sk):
    locFound = False
    if searchType != 3:
        citySpecific = input("Do you want to see tours in a specific city? (y/n): ")
        if citySpecific == "y":
            cityState =  queryLocation()
        elif citySpecific == "n":
            return [[False,False], False]
        else:
            print("Unsupported response. answers can be y or n")
            return [[False,False], False]
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