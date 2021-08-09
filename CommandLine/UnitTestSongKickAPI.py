import SongKickAPI
import unittest


class Test_SongKickAPI(unittest.TestCase):
    def test_findArtist(self):
        sk = SongKickAPI.SongKickAPI()
        # Test Success
        self.assertEqual(sk.find_artist("The Killers")[1]['id'],  555021)
        # Test Failure to find
        self.assertEqual(sk.find_artist("asdfl;kjkjbav")[0], "Failure")
        # Need to find 2 bands with same name to test edge case

    def test_findLocation(self):
        sk = SongKickAPI.SongKickAPI()
        # Test Success finding City
        self.assertEqual(sk.find_city("Los Angeles", "CA"), ["Success", 17835])
        # Test Failure to find
        self.assertEqual(sk.find_city("Philadelphasdf", "CA")[0], "Failure")
        # Need to find 2 bands with same name to test edge case


if __name__ == 'main':
    unittest.main()
