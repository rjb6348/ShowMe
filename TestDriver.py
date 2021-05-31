import MusicLibrary


def testSpotify():
    client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
    client_secret = '0d1c6411f69342359bdaca85134120eb'
    redirect_uri = 'http://localhost'

    ml = MusicLibrary.SpotifyInteractions(client_id, client_secret, redirect_uri)

    login_status = ml.login()
    check_status("Login", login_status)

    ml.dispUser()

    [TopArtists, TopArtist_status] = ml.pullUserTopArtists(limit=10)
    check_status("Pull Tracks", TopArtist_status)
    print("Number\tArtist")
    for i, item in enumerate(TopArtists['items']):
        print (i+1,'\t',item['name']) 

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