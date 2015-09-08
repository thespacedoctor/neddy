#!/usr/local/bin/python
# encoding: utf-8
"""
_basesearch.py
==============
:Summary:
    The base class for NED searches

:Author:
    David Young

:Date Created:
    May 6, 2015

:dryx syntax:
    - ``_someObject`` = a 'private' object that should only be changed for debugging

:Notes:
    - If you have any questions requiring this script/module please email me: d.r.young@qub.ac.uk

:Tasks:
    @review: when complete pull all general functions and classes into dryxPython
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import codecs
import re
import string
import csv
from docopt import docopt
from dryxPython import astrotools as dat
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
# from ..__init__ import *


###################################################################
# CLASSES                                                         #
###################################################################
class _basesearch:

    """
    The worker class for the NED _basesearch module

    **Key Arguments:**
        - ``log`` -- logger
    """
    # Initialisation

    def __init__(
        self
    ):
        return None

    def _convert_coordinates_to_decimal_degrees(
            self):
        """convert coordinates to decimal degrees

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _convert_coordinates_to_decimal_degrees method
            - @review: when complete add logging
            - @soon: fold in the code from astrotools to remove dependence
            - @soon: make a snippet for this method for future classes
        """
        self.log.info(
            'starting the ``_convert_coordinates_to_decimal_degrees`` method')

        from dryxPython import astrotools as dat

        try:
            self.raDeg = float(self.ra)
        except:
            self.raDeg = dat.ra_sexegesimal_to_decimal.ra_sexegesimal_to_decimal(
                ra=ra)
        try:
            self.decDeg = float(self.dec)
        except:
            self.decDeg = dat.declination_sexegesimal_to_decimal.declination_sexegesimal_to_decimal(
                dec=self.dec)

        self.log.info(
            'completed the ``_convert_coordinates_to_decimal_degrees`` method')
        return None

    # use the tab-trigger below for new method
    def _parse_the_ned_position_results(
            self):
        """ parse the ned results

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _parse_the_ned_results method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_parse_the_ned_results`` method')

        results = []
        headers = ["objectName", "objectType", "raDeg", "decDeg",
                   "redshift", "redshiftFlag", "arcminSeparation", "sepN", "sepE"]
        if self.nedResults:
            pathToReadFile = self.nedResults
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='rb')
                thisData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()

            matchObject = re.search(
                r"No\.\|Object Name.*?\n(.*)", thisData, re.S)
            if matchObject:
                # Print the header for stdout
                thisHeader = "| "
                for head in headers:
                    thisHeader += str(head).ljust(self.resultSpacing,
                                                  ' ') + " | "
                if not self.quiet:
                    print thisHeader
                theseLines = string.split(matchObject.group(), '\n')
                csvReader = csv.DictReader(
                    theseLines, dialect='excel', delimiter='|', quotechar='"')
                for row in csvReader:
                    thisDict = {}
                    thisRow = "| "
                    thisDict["raDeg"] = row["RA(deg)"].strip()
                    thisDict["decDeg"] = row["DEC(deg)"].strip()
                    thisDict["redshift"] = row["Redshift"].strip()
                    thisDict["redshiftFlag"] = row["Redshift Flag"].strip()
                    thisDict["objectName"] = row["Object Name"].strip()
                    thisDict["objectType"] = row["Type"].strip()
                    thisDict["arcminSeparation"] = row[
                        "Distance (arcmin)"].strip()

                    angularSeparation, northSep, eastSep = dat.get_angular_separation(
                        log=self.log,
                        ra1=self.ra,
                        dec1=self.dec,
                        ra2=thisDict["raDeg"],
                        dec2=thisDict["decDeg"]
                    )

                    thisDict["arcminSeparation"] = angularSeparation
                    thisDict["sepN"] = northSep
                    thisDict["sepE"] = eastSep

                    results.append(thisDict)
                    for head in headers:
                        thisRow += str(thisDict[head]
                                       ).ljust(self.resultSpacing, ' ') + " | "
                    if not self.quiet:
                        print thisRow
                    if self.nearestOnly:
                        break
            else:
                for head in headers:
                    thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
                if not self.quiet:
                    print thisRow
        else:
            # Print the header for stdout
            thisHeader = "| "
            for head in headers:
                thisHeader += str(head).ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print thisHeader
            thisRow = "| "
            for head in headers:
                thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print thisRow

        self.log.info('completed the ``_parse_the_ned_results`` method')
        return results

    # use the tab-trigger below for new method
    def _parse_the_ned_object_results(
            self):
        """ parse the ned results

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _parse_the_ned_results method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_parse_the_ned_results`` method')

        results = []
        headers = ["objectName", "objectType", "raDeg", "decDeg",
                   "redshift", "redshiftFlag"]
        if self.nedResults:
            pathToReadFile = self.nedResults
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='rb')
                thisData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()

            matchObject = re.search(
                r"No\.\|Object Name.*?\n(.*)", thisData, re.S)
            if matchObject:
                # Print the header for stdout
                thisHeader = "| "
                for head in headers:
                    thisHeader += str(head).ljust(self.resultSpacing,
                                                  ' ') + " | "
                if not self.quiet:
                    print thisHeader
                theseLines = string.split(matchObject.group(), '\n')
                csvReader = csv.DictReader(
                    theseLines, dialect='excel', delimiter='|', quotechar='"')
                for row in csvReader:
                    thisDict = {}
                    thisRow = "| "
                    thisDict["raDeg"] = row["RA(deg)"].strip()
                    thisDict["decDeg"] = row["DEC(deg)"].strip()
                    thisDict["redshift"] = row["Redshift"].strip()
                    thisDict["redshiftFlag"] = row["Redshift Flag"].strip()
                    thisDict["objectName"] = row["Object Name"].strip()
                    thisDict["objectType"] = row["Type"].strip()

                    results.append(thisDict)
                    for head in headers:
                        thisRow += str(thisDict[head]
                                       ).ljust(self.resultSpacing, ' ') + " | "
                    if not self.quiet:
                        print thisRow

            else:
                for head in headers:
                    thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
                if not self.quiet:
                    print thisRow
        else:
            # Print the header for stdout
            thisHeader = "| "
            for head in headers:
                thisHeader += str(head).ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print thisHeader
            thisRow = "| "
            for head in headers:
                thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print thisRow

        self.log.info('completed the ``_parse_the_ned_results`` method')
        return results

        # use the tab-trigger below for new method
    def _convert_html_to_csv(
            self):
        """ contert html to csv

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _convert_html_to_csv method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_convert_html_to_csv`` method')

        import codecs
        allData = ""
        regex1 = re.compile(
            r'.*<PRE><strong>   (.*?)</strong>(.*?)</PRE></TABLE>.*', re.I | re.S)
        regex2 = re.compile(r'\|(\w)\|', re.I | re.S)
        for thisFile in self.nedResults:
            pathToReadFile = thisFile
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='r')
                thisData = readFile.read()
                readFile.close()
            except IOError, e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()

            self.log.debug("regex 1 - sub")
            thisData = regex1.sub("\g<1>\g<2>", thisData)
            self.log.debug("regex 2 - sub")
            thisData = regex2.sub("abs(\g<1>)", thisData)
            self.log.debug("replace text")
            thisData = thisData.replace("|b|", "abs(b)")

            writeFile = codecs.open(pathToReadFile, encoding='utf-8', mode='w')
            writeFile.write(thisData)
            writeFile.close()

        self.log.info('completed the ``_convert_html_to_csv`` method')
        return None

    # use the tab-trigger below for new method
    def _parse_the_ned_list_results(
            self):
        """ parse the ned results

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _parse_the_ned_results method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_parse_the_ned_list_results`` method')

        results = []
        headers = ["row_number", "input_note", "input_name", "ned_notes", "ned_name", "ra", "dec", "eb-v", "object_type", "redshift", "redshift_err", "redshift_quality", "magnitude_filter",
                   "major_diameter_arcmin", "minor_diameter_arcmin", "morphology", "hierarchy", "galaxy_morphology", "radio_morphology", "activity_type", "distance_indicator", "distance_mod", "distance", "row_number"]

        for thisFile in self.nedResults:
            if thisFile:
                pathToReadFile = thisFile
                try:
                    self.log.debug("attempting to open the file %s" %
                                   (pathToReadFile,))
                    readFile = codecs.open(
                        pathToReadFile, encoding='utf-8', mode='rb')
                    thisData = readFile.read()
                    readFile.close()
                except IOError, e:
                    message = 'could not open the file %s' % (pathToReadFile,)
                    self.log.critical(message)
                    raise IOError(message)
                readFile.close()

                matchObject = re.search(
                    r"\n(1\s*?\|\s*?.*)", thisData, re.S)
                if matchObject:
                    # Print the header for stdout
                    thisHeader = ""
                    for head in headers:
                        thisHeader += str(head).ljust(self.resultSpacing,
                                                      ' ') + " | "

                    theseLines = string.split(matchObject.group(), '\n')
                    theseLines = [thisHeader] + theseLines
                    thisHeader = "| " + thisHeader
                    if not self.quiet:
                        print thisHeader
                    csvReader = csv.DictReader(
                        theseLines, dialect='excel', delimiter='|', quotechar='"')
                    for row in csvReader:
                        thisRow = "| "
                        thisDict = {}
                        row = dict(row)
                        for k, v in row.iteritems():
                            try:
                                # self.log.debug("attempting to strip ned key")
                                k = k.strip()
                            except Exception, e:
                                self.log.error(
                                    'cound not strip ned key (%(k)s, %(v)s)' % locals())
                                self.log.error(
                                    "could not strip ned key - failed with this error: %s " % (str(e),))
                                return -1
                            if (k == "ra" or k == "dec"):
                                v = v.replace("h", ":").replace(
                                    "m", ":").replace("d", ":").replace("s", "")
                            if isinstance(v, str):
                                v = v.strip()
                            thisDict[k] = v
                        results.append(thisDict)
                        for head in headers:
                            thisRow += str(thisDict[head]
                                           ).ljust(self.resultSpacing, ' ') + " | "
                        if not self.quiet:
                            print thisRow

                else:
                    for head in headers:
                        thisRow += str("").ljust(self.resultSpacing,
                                                 ' ') + " | "
                    if not self.quiet:
                        print thisRow
            else:
                # Print the header for stdout
                thisHeader = "| "
                for head in headers:
                    thisHeader += str(head).ljust(self.resultSpacing,
                                                  ' ') + " | "
                if not self.quiet:
                    print thisHeader
                thisRow = "| "
                for head in headers:
                    thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
                if not self.quiet:
                    print thisRow

        self.log.info('completed the ``_parse_the_ned_list_results`` method')
        return results

    def _split_incoming_queries_into_batches(
            self,
            sources):
        """ split incoming queries into batches

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _split_incoming_queries_into_batches method
            - @review: when complete add logging
        """
        self.log.info(
            'starting the ``_split_incoming_queries_into_batches`` method')

        batchSize = 300
        total = len(sources)
        batches = int(total / batchSize) + 1

        start = 0
        end = 0
        theseBatches = []
        for i in range(batches):
            end = end + batchSize
            start = i * batchSize
            thisBatch = sources[start:end]
            theseBatches.append(thisBatch)

        self.log.info(
            'completed the ``_split_incoming_queries_into_batches`` method')
        return theseBatches

        # use the tab-trigger below for new method
        # xt-class-method
