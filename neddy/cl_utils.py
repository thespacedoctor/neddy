#!/usr/bin/env python
# encoding: utf-8
"""
Documentation for neddy can be found here: http://neddy.readthedocs.org

Usage:
    neddy [-nuvr] cone (filelist <pathToCoordinateList> <radiusArcsec> | <ra> <dec> <radiusArcsec>) [<outPutFile>]
    neddy [-v] obj <objectName> [<objectName>...]
    
    -h, --help            show this help message
    -n, --nearest         nearest object only
    -u, --unclassified    include unclassifed extra-galaxtic objects
    -v, --verbose         return more metadata for matches
    -r, --redshift        redshift must be available
    ra                    ra (decimal degrees or sexegesimal)
    dec                   dec (decimal degrees or sexegesimal)
    radiusArcsec          radiusArcsec (conesearch radius)
    objectName            objectName (the name of the object)
    pathToCoordinateList  path to list of ra dec radiusArcsec
    outPutFile            path to outputfile
"""
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=False,
        projectName="neddy",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

    # tab completion for raw_input
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    # UNPACK REMAINING CL ARGUMENTS USING `EXEC` TO SETUP THE VARIABLE NAMES
    # AUTOMATICALLY
    a = {}
    for arg, val in list(arguments.items()):
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        a[varname] = val
        if arg == "--dbConn":
            dbConn = val
            a["dbConn"] = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    # set options interactively if user requests
    if "interactiveFlag" in a and a["interactiveFlag"]:

        # load previous settings
        moduleDirectory = os.path.dirname(__file__) + "/resources"
        pathToPickleFile = "%(moduleDirectory)s/previousSettings.p" % locals()
        try:
            with open(pathToPickleFile):
                pass
            previousSettingsExist = True
        except:
            previousSettingsExist = False
        previousSettings = {}
        if previousSettingsExist:
            previousSettings = pickle.load(open(pathToPickleFile, "rb"))

        # x-raw-input
        # x-boolean-raw-input
        # x-raw-input-with-default-value-from-previous-settings

        # save the most recently used requests
        pickleMeObjects = []
        pickleMe = {}
        theseLocals = locals()
        for k in pickleMeObjects:
            pickleMe[k] = theseLocals[k]
        pickle.dump(pickleMe, open(pathToPickleFile, "wb"))

    if a["init"]:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/neddy/neddy.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        return

    ra = a["ra"]
    dec = a["dec"]
    radiusArcsec = a["radiusArcsec"]
    objectName = a["objectName"]
    pathToCoordinateList = a["pathToCoordinateList"]
    outPutFile = a["outPutFile"]
    nearest = a["nearest"]
    unclassified = a["unclassified"]
    redshift = a["redshift"]

    # CALL FUNCTIONS/OBJECTS
    if cone and filelist:
        import codecs
        pathToReadFile = pathToCoordinateList
        readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')

        listOfCoordinates = []
        for line in readFile.readlines():
            line = line.strip()
            [ra, dec] = line.split()
            listOfCoordinates.append(str(ra) + " " + str(dec))
        search = conesearch(
            log=log,
            radiusArcsec=radiusArcsec,
            nearestOnly=nearestFlag,
            unclassified=unclassifiedFlag,
            listOfCoordinates=listOfCoordinates,
            outputFilePath=outPutFile,
            verbose=verboseFlag,
            redshift=redshiftFlag)
    elif cone:
        search = conesearch(
            log=log,
            ra=ra,
            dec=dec,
            radiusArcsec=radiusArcsec,
            nearestOnly=nearestFlag,
            unclassified=unclassifiedFlag,
            outputFilePath=outPutFile,
            verbose=verboseFlag,
            redshift=redshiftFlag
        )
    elif obj:
        search = namesearch(
            log=log,
            names=objectName,
            verbose=verboseFlag,
            outputFilePath=outPutFile
        )
    search.get()

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()
