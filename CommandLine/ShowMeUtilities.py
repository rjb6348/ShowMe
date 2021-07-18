import datetime
from pyzipcode import ZipCodeDatabase
import MusicLibrary


def setup_music_library():
    print("Time to Login to Spotify!")
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://192.168.0.143:8000/'
    logged_in = False
    try:
        music_library = MusicLibrary.SpotifyUserInteractions(
            client_id, client_secret, redirect_uri)
        while logged_in is False:
            user_name = input("What's your username: ")
            login_status = music_library.login(user_name)
            if login_status.lower() != "success":
                print("Login Failed.")
                again = input("Try again (y/n): ")
                if again == 'n':
                    break
            else:
                logged_in = True
        return music_library
    except:
        print("Login Failed Unexpectedly")
        return False


def check_to_query_location(search_type, song_kick):
    loc_found = False
    if search_type != 2:
        again = True
        while again is True:
            city_specific = input(
                "Do you want to see tours in a specific city? (y/n): ")
            if city_specific.lower() == "y":
                city_state = query_location()
                if city_state == [False, False]:
                    return [[False, False], False]
                again = False
            elif city_specific.lower() == "n":
                return [[False, False], False]
            else:
                print("Waning:  Unrecognized input. Only y or n accepted")
    else:
        city_state = query_location()
        if city_state == [False, False]:
            return [[False, False], False]
    while loc_found is False:
        [loc_status, loc_id] = song_kick.find_city(
            city_state[0], city_state[1])
        if loc_status.lower() == 'success':
            loc_found = True
        else:
            print("City, State Combination not found.")
            again = again_query()
            if again:
                city_state = query_location()
            else:
                return False
    return [city_state, loc_id]


def query_location():
    results = query_standard(["City & State", "Zip"])
    if results is False:
        search_query = [False, False]
    elif results == 1:
        state = input("Enter two letter State Abbreviation (ex: PA): ")
        city = input("Enter the City: ")
        search_query = [city, state]
    elif results == 2:
        zcdb = ZipCodeDatabase()
        zip_found = False
        while zip_found is False:
            try:
                zip_int = input("Enter Zip Code: ")
                zipcode = zcdb[int(zip_int)]
                zip_found = True
            except:
                print("Zip " + zip_int + " not found.")
                again = again_query()
                if again:
                    continue
                else:
                    return [False, False]
        search_query = [zipcode.city, zipcode.state]
    else:
        print("I do not understand how we got here")
        search_query = [False, False]
    return search_query


def query_date_range():
    again = True
    while again is True:
        date_filter = input("Do you want to search results by Date? (y/n) ")
        if date_filter.lower() == "y":
            again = False
        elif date_filter.lower() == "n":
            return [False, False]
        else:
            print("Waning:  Unrecognized input. Only y or n accepted")
    start_date_good = False
    while start_date_good is False:
        print('What date do you want to start searching from? (mm/dd/yyyy)')
        start_date = input("Start Date: ")
        try:
            month1, day1, year1 = start_date.split('/')
            date1 = datetime.datetime(int(year1), int(month1), int(day1))
            if date1 < datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0)):
                print("Warning: Start date needs to be after today")
            else:
                start_date_good = True
        except ValueError:
            print("Warning: Start Date " + start_date +
                  " not in correct format (mm/dd/yyyy)")
    end_date_good = False
    while end_date_good is False:
        print('What date do you want to stop searching from? (mm/dd/yyyy)')
        end_date = input("Stop Date: ")
        try:
            month2, day2, year2 = end_date.split('/')
            date2 = datetime.datetime(int(year2), int(month2), int(day2))
            if date2 > date1:
                end_date_good = True
                start_date = "-".join([year1, month1, day1])
                end_date = "-".join([year2, month2, day2])
            else:
                print("Warning: End date has to be after start date of: " + str(date1))
        except ValueError:
            print("Warning: End Date " + end_date +
                  " not in correct format (mm/dd/yyyy)")

    return [start_date, end_date]


def prompt_for_search_type():
    results = query_standard(
        ["Search by Artist", "Search by Location", "Search by Music Library"])
    return results


def create_search_type_query(search_type):
    search_query = []
    results = []
    if search_type == 1:
        results = input(
            "What is the artist/band you want to find a tour for?: ")
    elif search_type == 3:
        search_query = ["Top Artists from Long Term", "Top Artist from Medium Term",
                        "Top Artist from Short Term", "Top Artists from each period"]
        results = query_standard(search_query)
        if int(results) in range(1, 5):
            if int(results) == 1:
                results = ["long_term"]
            elif int(results) == 2:
                results = ["medium_term"]
            elif int(results) == 3:
                results = ["long_term"]
            elif int(results) == 4:
                results = ["long_term", "medium_term", "short_term"]
    return results


def again_query():
    again = True
    while again is True:
        again_in = input("Try again (y/n): ")
        if again_in.lower() == 'n':
            return False
        elif again_in.lower() == 'y':
            return True
        else:
            print("Waning:  Unrecognized input. Only y or n accepted")


def query_standard(options):
    result = None
    while result is None:
        print("Do you want to search by: ")
        for i in range(1, len(options)+1):
            print(str(i) + ": " + options[i-1])
        input_string = input("Search By: ")

        if input_string is None or input_string == "":
            print("Warning: No input selected.")
            again = again_query()
            if again:
                continue
            else:
                return False
        elif input_string.isnumeric() is False or int(input_string) not in range(1, len(options)+1):
            print("Warning: Enter a number betwee 1 and " + str(len(options)))
            again = again_query()
            if again:
                continue
            else:
                return False
        elif int(input_string) in range(1, len(options)+1):
            return int(input_string)
        else:
            print("Unhandled Input")
            return False
