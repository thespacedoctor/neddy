import os
import nose
import shutil
from neddy import conesearch
from neddy.utKit import utKit


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# xnose-class-to-test-main-command-line-function-of-module


class test_conesearch(unittest.TestCase):

    def test_conesearch_function(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["ra"] = 204.253833
        kwargs["dec"] = -29.865750
        kwargs["radiusArcsec"] = 15
        kwargs["nearestOnly"] = False
        kwargs["unclassified"] = True
        testObject = conesearch(**kwargs)
        testObject.get()

    def test_conesearch_function_02(self):

        import codecs
        pathToReadFile = pathToInputDir + "/coordinates.txt"
        readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')

        listOfCoordinates = []
        for line in readFile.readlines():
            line = line.strip()
            [ra, dec] = line.split()
            listOfCoordinates.append(str(ra) + " " + str(dec))

        kwargs = {}
        kwargs["log"] = log
        kwargs["nearestOnly"] = False
        kwargs["unclassified"] = True
        kwargs["radiusArcsec"] = 29
        kwargs["listOfCoordinates"] = listOfCoordinates
        testObject = conesearch(**kwargs)
        testObject.get()

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
