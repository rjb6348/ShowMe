import ShowMeUtilities
import unittest
import SongKickAPI
class Test_SongKickAP(unittest.TestCase):
    #ML Section
    def test_setupMLPass(self):
        # Has to be run locally for now
        inputValuesGood = [ 'rrbvt']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesGood.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.setupML(3)
        self.assertNotEqual(result,False)
    '''
    def test_setupMFail(self):
        #Test Failure to find
        inputValuesBad = [ 'asdf;lkasdf;lkasdf','asdflkj;asdf;lkj']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesBad.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.setupML(3)
        self.assertEqual(result,False)
    '''
    #queryLocation Section
    def test_queryLocationZipGood(self):
        failVals = [False, False]
        inputValuesYesZipValid = ['2','19147']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesYesZipValid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryLocation()
        self.assertEqual(result,['Philadelphia','PA'])

    def test_queryLocationZipBad(self):
        failVals = [False, False]
        inputValuesYesZipValid = ['2','191470','n']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesYesZipValid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryLocation()
        self.assertEqual(result,failVals)

    def test_queryLocationCity(self):
        failVals = [False, False]
        inputValuesCity = ['1','PA', 'Philadelphia']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesCity.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryLocation()
        self.assertEqual(result,['Philadelphia','PA' ])

    #checkToQueryLocationN Section
    def test_checkToQueryLocationN(self):
        sk = SongKickAPI.SongKickAPI()
        failVals = [[False, False], False]
        inputValuesNo = ['n']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesNo.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.checkToQueryLocation(3,sk)
        self.assertEqual(result,failVals)

    def test_checkToQueryLocationYGoodZip(self):
        sk = SongKickAPI.SongKickAPI()
        failVals = [[False, False], False]

        inputValuesYesZipValid = ['y','2','19147']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesYesZipValid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.checkToQueryLocation(1,sk)
        self.assertNotEqual(result,failVals)

    def test_checkToQueryLocationYBadZip(self):
        sk = SongKickAPI.SongKickAPI()
        failVals = [[False, False], False]
        inputValuesYesZipInvalid = ['y','2','19000','n']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesYesZipInvalid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.checkToQueryLocation(1,sk)
        self.assertEqual(result,failVals)

    def test_checkToQueryLocationYGoodCity(self):
        sk = SongKickAPI.SongKickAPI()
        failVals = [[False, False], False]
        inputValuesNoCityValid = ['y','1','PA','Philadelphia']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesNoCityValid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.checkToQueryLocation(1,sk)
        self.assertNotEqual(result,failVals)

    def test_checkToQueryLocationYBadCity(self):
        sk = SongKickAPI.SongKickAPI()
        failVals = [[False, False], False]
        inputValuesNoCityInvalid = ['y','1','CA','Philadelphia','n']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputValuesNoCityInvalid.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.checkToQueryLocation(2,sk)
        self.assertEqual(result,failVals)


    def test_queryStandard1(self):
        inputArtist = ["1"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputArtist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
        self.assertEqual(result, 1)

    def test_queryStandard2(self):
        inputArtist = ["2"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputArtist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
        self.assertEqual(result, 2)

    def test_queryStandard3(self):
        inputArtist = ["3"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputArtist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
        self.assertEqual(result, 3)

    def test_queryStandardFail(self):
        inputArtist = ["4",'n']
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputArtist.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.queryStandard(["Search by Artist","Search by Location","Search by Music Library"])
        self.assertEqual(result, False)

    def test_againy(self):
        inputagain = ["y"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputagain.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.againQuery()
        self.assertEqual(result, True)

    def test_againn(self):
        inputagain = ["n"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputagain.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.againQuery()
        self.assertEqual(result, False)

    def test_againInvalid(self):
        inputagain = ["","","y"]
        outputFail = []
        def mock_input(s):
            outputFail.append(s)
            return inputagain.pop(0)
        ShowMeUtilities.input = mock_input
        ShowMeUtilities.print = lambda s : outputFail.append(s)
        result = ShowMeUtilities.againQuery()
        self.assertEqual(result, True)

if __name__ == 'main':
    unittest.main()
