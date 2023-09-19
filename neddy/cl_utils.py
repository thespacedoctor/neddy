#!/usr/bin/env python
# encoding: utf-8
"""
Documentation for neddy can be found here: http://neddy.readthedocs.org

Usage:
    neddy init
    neddy [-nuvr] cone <ra> <dec> <radiusArcsec> [--o <outputFile>]
    neddy [-nuvr] cones <pathToCoordinateList> <radiusArcsec> [--o <outputFile>]
    neddy [-v] name <objectName> [<objectName>...] [--o <outputFile>]

Commands:    
    init                  initialise neddy for the first time
    cone                  perform a single conesearch on NED and return any matches
    cones                 perform bulk conesearches on NED and return any matches
    name                  perform name search(es) on NED and return any matches

Arguments:
    ra                    ra (decimal degrees or sexegesimal)
    dec                   dec (decimal degrees or sexegesimal)
    radiusArcsec          radiusArcsec (conesearch radius)
    objectName            objectName (the name of the object)
    pathToCoordinateList  path to list of space separated ra & dec (one coordinate set per line, decimal degrees or sexegesimal)
    --o outputFile        path to outputFile 
    
Options:
    -h, --help            show this help message
    -n, --nearest         return the nearest object only
    -u, --unclassified    include unclassified extra-galactic objects
    -v, --verbose         return more metadata for matches
    -r, --redshift        redshift must be available
"""
from subprocess import Popen, PIPE, STDOUT
from fundamentals import tools, times
from docopt import docopt
import pickle
import glob
import readline
from builtins import str
import sys
import os
os.environ['TERM'] = 'vt100'


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when `cl_utils.py` is run as a single script from the cl, or when installed as a cl command*
    """
    # SETUP THE COMMAND-LINE UTIL SETTINGS
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=False,
        projectName="neddy",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

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

    # UNPACK USEAGE COMMANDS & ARGUMENTS
    ra = a["ra"]
    dec = a["dec"]
    radiusArcsec = a["radiusArcsec"]
    objectName = a["objectName"]
    name = a["name"]
    pathToCoordinateList = a["pathToCoordinateList"]
    outputFile = a["oFlag"]
    nearestFlag = a["nearestFlag"]
    unclassifiedFlag = a["unclassifiedFlag"]
    redshiftFlag = a["redshiftFlag"]
    verboseFlag = a["verboseFlag"]
    cone = a["cone"]
    cones = a["cones"]

    # CALL FUNCTIONS/OBJECTS
    if cones:
        import codecs
        pathToReadFile = pathToCoordinateList
        readFile = codecs.open(pathToReadFile, encoding='utf-8', mode='r')

        listOfCoordinates = []
        for line in readFile.readlines():
            line = line.strip()
            [ra, dec] = line.split()
            listOfCoordinates.append(str(ra) + " " + str(dec))
        from .conesearch import conesearch
        search = conesearch(
            log=log,
            radiusArcsec=radiusArcsec,
            nearestOnly=nearestFlag,
            unclassified=unclassifiedFlag,
            listOfCoordinates=listOfCoordinates,
            outputFilePath=outputFile,
            verbose=verboseFlag,
            redshift=redshiftFlag)
    elif cone:
        from .conesearch import conesearch
        search = conesearch(
            log=log,
            ra=ra,
            dec=dec,
            radiusArcsec=radiusArcsec,
            nearestOnly=nearestFlag,
            unclassified=unclassifiedFlag,
            outputFilePath=outputFile,
            verbose=verboseFlag,
            redshift=redshiftFlag
        )
    elif name:
        from .namesearch import namesearch
        search = namesearch(
            log=log,
            names=objectName,
            verbose=verboseFlag,
            outputFilePath=outputFile
        )
    results = search.get()

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
