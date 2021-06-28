import SongKickAPI
import unittest


class Test_SongKickAPI(unittest.TestCase):
    def test_findArtist(self):
        sk = SongKickAPI.SongKickAPI()
        # Test Success
        self.assertEqual(sk.findArtist("The Killers"), ["Success", 555021])
        # Test Failure to find
        self.assertEqual(sk.findArtist("asdfl;kjkjbav")[0], "Failure")
        # Need to find 2 bands with same name to test edge case

    def test_findLocation(self):
        sk = SongKickAPI.SongKickAPI()
        # Test Success finding City
        self.assertEqual(sk.findCity("Los Angeles", "CA"), ["Success", 17835])
        # Test Failure to find
        self.assertEqual(sk.findCity("Philadelphasdf", "CA")[0], "Failure")
        # Need to find 2 bands with same name to test edge case


if __name__ == 'main':
    unittest.main()
