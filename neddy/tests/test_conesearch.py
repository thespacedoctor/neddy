from __future__ import print_function
from builtins import str
import os
import unittest
import shutil
import yaml
from neddy.utKit import utKit
from fundamentals import tools
from os.path import expanduser
home = expanduser("~")

packageDirectory = utKit("").get_project_root()
settingsFile = packageDirectory + "/test_settings.yaml"

su = tools(
    arguments={"settingsFile": settingsFile},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName=None,
    defaultSettingsFile=False
)
arguments, settings, log, dbConn = su.setup()

# SETUP PATHS TO COMMON DIRECTORIES FOR TEST DATA
moduleDirectory = os.path.dirname(__file__)
pathToInputDir = moduleDirectory + "/input/"
pathToOutputDir = moduleDirectory + "/output/"

try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)


class test_conesearch(unittest.TestCase):

    def test_conesearch_function(self):
        from neddy import conesearch
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
        from neddy import conesearch
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
