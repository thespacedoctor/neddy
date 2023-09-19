from __future__ import print_function
from builtins import str
import os
import unittest
import shutil
import yaml
from neddy.utKit import utKit
from fundamentals import tools
from os.path import expanduser
from docopt import docopt
from neddy import cl_utils
doc = cl_utils.__doc__
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

# RECURSIVELY CREATE MISSING DIRECTORIES
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)


class test_cl_utils(unittest.TestCase):

    import pytest

    def test_init(self):
        # TEST INITIALISATION OF NEDDY
        command = "neddy init"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)
        return

    @pytest.mark.full
    def test_conesearch(self):
        # RUN A SINGLE CONESEARCH ON NED
        command = "neddy cone 02:27:16.9 +33:34:45 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # RETURN A MORE VERBOSE OUTPUT
        command = "neddy -v cone 02:27:16.9 +33:34:45 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # RETURN THE NEAREST OBJECT ONLY
        command = "neddy -n cone 02:27:16.9 +33:34:45 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # INCLUDE UNCLASSIFIED EXTRA-GALACTIC OBJECTS
        command = "neddy -u cone 02:27:16.9 +33:34:45 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # REDSHIFT MUST BE AVAILABLE
        command = "neddy -r cone 02:27:16.9 +33:34:45 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # WRITE THE RESULTS TO FILE
        command = f"neddy -r cone 02:27:16.9 +33:34:45 4.0 --o {pathToOutputDir}/results.csv"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)
        return

    def test_conesearch_all(self):
        # RUN A SINGLE CONESEARCH ON NED
        command = f"neddy -vnur cone 02:27:16.9 +33:34:45 4.0 --o {pathToOutputDir}/results.csv"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

    def test_conesearches(self):
        # RUN MULTIPLE NED CONESEARCHES
        command = f"neddy -vn cones {pathToOutputDir}/coordinates.txt 4.0"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # RUN MULTIPLE NED CONESEARCHES AND OUTPUT TO FILE
        command = f"neddy -vn cones {pathToOutputDir}/coordinates.txt 4.0 --o {pathToOutputDir}/results.csv"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)
        return

    def test_name_searches(self):
        # RUN A SINGLE NED NAME SEARCH
        command = f"neddy -v name m31"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # RUN MULTIPLE NED NAME SEARCHES
        command = f"neddy -v name m31 m51 m101"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)

        # RUN MULTIPLE NED NAME SEARCHES AND OUTPUT TO FILE
        command = f"neddy -v name m31 m51 m101 --o {pathToOutputDir}/results.csv"
        args = docopt(doc, command.split(" ")[1:])
        cl_utils.main(args)
        return

    # x-class-to-test-named-worker-function
