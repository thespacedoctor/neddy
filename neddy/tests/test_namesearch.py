import os
import nose
import shutil
import yaml
from neddy import namesearch
from neddy.utKit import utKit


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()


class test_namesearch():

    def test_namesearch_function(self):
        kwargs = {}
        kwargs["log"] = log
        kwargs["names"] = "CXO J133700.87-295156.2"
        testObject = namesearch(**kwargs)
        testObject.get()

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
