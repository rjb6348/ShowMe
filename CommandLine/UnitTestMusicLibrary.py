import MusicLibrary
import unittest
client_id = '1b55c01382b740c0b4c6fd22f7065fd6'
client_secret = '0d1c6411f69342359bdaca85134120eb'
redirect_uri = 'http://localhost'
'''
class Test_MusicLibrary(unittest.TestCase):

TODO: Need to switch to using cache_path if want to unit test
    Note: Would be better unit testing if used artist lookup which doesn't require login 
    def test_login(self):
        ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
        #Test Success
        self.assertEqual(ml.login("rrbvt"),"Success")
        #Test Displaying User
        self.assertEqual(ml.dispUser(), "rrbvt")

    def test_pullArtists(self):
        ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
        #Test Success finding City
        ml.login("rrbvt")
        self.assertEqual(ml.pullUserTopArtists(limit=20),len(20))
        self.assertEqual(ml.pullUserTopArtists(limit=30),len(30))
        self.assertNotEqual(ml.pullUserTopArtists(limit=10),ml.pullUserTopArtists(limit=10,offset=10))
        
    def test_logout(self):
        ml = MusicLibrary.SpotifyUserInteractions(client_id, client_secret, redirect_uri)
        #Test Success finding City
        ml.login("rrbvt")
        #ml.logout()
'''

if __name__ == 'main':
    unittest.main()

        
