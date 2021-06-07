import MusicLibrary
import SongKickAPI

def testSpotify():
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'

    ml = MusicLibrary.SpotifyInteractions(client_id, client_secret, redirect_uri)

    login_status = ml.login('rrbvt')
    check_status("Login", login_status)

    ml.dispUser()

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10)
    check_status("Pull Tracks", TopArtist_status)
    print("Long_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10,time_range="medium_term")
    check_status("Pull Tracks", TopArtist_status)
    print("Medium_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10,time_range="short_term")
    check_status("Pull Tracks", TopArtist_status)
    print("Short_Term")
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 


def testSongKickApi():
    sk = SongKickAPI.SongKickAPI()
    artistId = sk.findArtist('The Killers')
    print(artistId)
    LocationId = sk.findCity('Philadelphia','PA')
    print(LocationId)
    Events = sk.findArtistEvents(artistId)
    print(Events)


def check_status(step, return_status):
    if return_status.lower() == "success":
        return
    elif return_status.lower() == "warning":
        return
    elif return_status.lower() == "error":
        raise Exception(["Step: " + step + " Errored"])
    else:
        Exception(["Unhandled Return Status: " + return_status])

if __name__ == "__main__":
    testSpotify()
    testSongKickApi()