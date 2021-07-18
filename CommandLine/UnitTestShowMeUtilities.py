import ShowMeUtilities
import unittest
import SongKickAPI


class Test_SongKickAP(unittest.TestCase):
    # ML Section
    def test_setupMLPass(self):
        # Has to be run locally for now
        input_values_good = ['rrbvt']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_good.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.setup_music_library()
        self.assertNotEqual(result, False)

    def test_query_location_zip_good(self):
        failVals = [False, False]
        input_values_yes_zip_valid = ['2', '19147']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_yes_zip_valid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_location()
        self.assertEqual(result, ['Philadelphia', 'PA'])

    def test_query_location_zip_bad(self):
        fail_vals = [False, False]
        input_values_yes_zip_valid = ['2', '191470', 'n']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_yes_zip_valid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_location()
        self.assertEqual(result, fail_vals)

    def test_query_location_city(self):
        input_values_city = ['1', 'PA', 'Philadelphia']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_city.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_location()
        self.assertEqual(result, ['Philadelphia', 'PA'])

    # checkToQueryLocationN Section
    def test_check_to_query_location_n(self):
        sk = SongKickAPI.SongKickAPI()
        fail_vals = [[False, False], False]
        input_values_no = ['n']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_no.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.check_to_query_location(3, sk)
        self.assertEqual(result, fail_vals)

    def test_check_to_query_location_y_good_zip(self):
        sk = SongKickAPI.SongKickAPI()
        fail_vals = [[False, False], False]

        input_values_yes_zip_valid = ['y', '2', '19147']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_yes_zip_valid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.check_to_query_location(1, sk)
        self.assertNotEqual(result, fail_vals)

    def test_check_to_query_location_y_bad_zip(self):
        song_kick = SongKickAPI.SongKickAPI()
        fail_vals = [[False, False], False]
        input_values_yes_zip_invalid = ['y', '2', '19000', 'n']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_yes_zip_invalid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.check_to_query_location(1, song_kick)
        self.assertEqual(result, fail_vals)

    def test_check_to_query_location_y_good_city(self):
        song_kick = SongKickAPI.SongKickAPI()
        fali_vals = [[False, False], False]
        input_values_no_city_valid = ['y', '1', 'PA', 'Philadelphia']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_no_city_valid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.check_to_query_location(1, song_kick)
        self.assertNotEqual(result, fali_vals)

    def test_check_to_query_location_y_bad_city(self):
        song_kick = SongKickAPI.SongKickAPI()
        fail_vals = [[False, False], False]
        input_values_no_city_invalid = ['y', '1', 'CA', 'Philadelphia', 'n']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_values_no_city_invalid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.check_to_query_location(2, song_kick)
        self.assertEqual(result, fail_vals)

    def test_query_standard_1(self):
        input_artist = ["1"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_artist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_standard(
            ["Search by Artist", "Search by Location", "Search by Music Library"])
        self.assertEqual(result, 1)

    def test_query_standard_2(self):
        input_artist = ["2"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_artist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_standard(
            ["Search by Artist", "Search by Location", "Search by Music Library"])
        self.assertEqual(result, 2)

    def test_query_standard_3(self):
        input_artist = ["3"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_artist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_standard(
            ["Search by Artist", "Search by Location", "Search by Music Library"])
        self.assertEqual(result, 3)

    def test_query_standard_fail(self):
        input_artist = ["4", 'n']
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_artist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.query_standard(
            ["Search by Artist", "Search by Location", "Search by Music Library"])
        self.assertEqual(result, False)

    def test_again_y(self):
        input_again = ["y"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_again.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.again_query()
        self.assertEqual(result, True)

    def test_again_n(self):
        input_again = ["n"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_again.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.again_query()
        self.assertEqual(result, False)

    def test_again_invalid(self):
        input_again = ["", "", "y"]
        output_fail = []

        def mock_input(s):
            output_fail.append(s)
            return input_again.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s: output_fail.append(s)
        result = ShowMeUtilities.again_query()
        self.assertEqual(result, True)


if __name__ == 'main':
    unittest.main()
