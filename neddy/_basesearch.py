#!/usr/local/bin/python
# encoding: utf-8
"""
*The base class for NED searches*

:Author:
    David Young
"""
from __future__ import print_function
from __future__ import division
from builtins import zip
from builtins import str
from builtins import range
from builtins import object
from past.utils import old_div
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import codecs
import re
import csv
from docopt import docopt
from astrocalc.coords import unit_conversion
from fundamentals import tools, times

class _basesearch(object):
    """
    The base-class for searching NED
    """
    # Initialisation

    def __init__(
        self
    ):
        return None

    def _convert_coordinates_to_decimal_degrees(
            self):
        """
        *convert coordinates to decimal degrees*
        """
        self.log.debug(
            'completed the ````_convert_coordinates_to_decimal_degrees`` method')

        converter = unit_conversion(
            log=self.log
        )

        # CONVERT ALL COORDINATES TO DECIMAL DEGREES
        if len(self.listOfCoordinates) and isinstance(self.listOfCoordinates[0], ("".__class__, u"".__class__)):
            sources = []
            sources[:] = [s.split(" ") for s in self.listOfCoordinates]

        else:
            sources = self.listOfCoordinates
        self.listOfCoordinates = []

        # TEST IF CONVERSION IS REQUIRED
        try:
            ra = float(sources[0][0])
            convert = False
        except:
            convert = True

        if convert == True:
            raDegs = []
            raDegs[:] = [converter.ra_sexegesimal_to_decimal(
                ra=s[0]) for s in sources]
            decDegs = []
            decDegs[:] = [converter.dec_sexegesimal_to_decimal(
                dec=s[1]) for s in sources]
            self.listOfCoordinates = []
            self.listOfCoordinates[:] = [[raDeg, decDeg]
                                         for raDeg, decDeg in zip(raDegs, decDegs)]

        else:
            self.listOfCoordinates = []
            self.listOfCoordinates[:] = [[float(s[0]), float(s[1])]
                                         for s in sources]

        self.log.debug(
            'completed the ``_convert_coordinates_to_decimal_degrees`` method')
        return None

    def _parse_the_ned_position_results(
            self,
            ra,
            dec,
            nedResults):
        """
        *parse the ned results*

        **Key Arguments**

        - ``ra`` -- the search ra
        - ``dec`` -- the search dec
        

        **Return**

        - ``results`` -- list of result dictionaries
        
        """
        self.log.debug('starting the ``_parse_the_ned_results`` method')

        results = []
        resultLen = 0
        if nedResults:
            # OPEN THE RESULT FILE FROM NED
            pathToReadFile = nedResults
            try:
                self.log.debug("attempting to open the file %s" %
                               (pathToReadFile,))
                readFile = codecs.open(
                    pathToReadFile, encoding='utf-8', mode='rb')
                thisData = readFile.read()
                readFile.close()
            except IOError as e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            readFile.close()

            # CHECK FOR ERRORS
            if "Results from query to  NASA/IPAC Extragalactic Database" not in thisData:
                print("something went wrong with the NED query")
                self.log.error(
                    "something went wrong with the NED query" % locals())
                sys.exit(0)

            # SEARCH FROM MATCHES IN RESULTS FILE
            matchObject = re.search(
                r"No\.\|Object Name.*?\n(.*)", thisData, re.S)
            if matchObject:
                theseLines = str.split(matchObject.group(), '\n')
                resultLen = len(theseLines)
                csvReader = csv.DictReader(
                    theseLines, dialect='excel', delimiter='|', quotechar='"')
                for row in csvReader:
                    thisEntry = {"searchRa": ra, "searchDec": dec,
                                 "matchName": row["Object Name"].strip()}
                    results.append(thisEntry)
                    if self.nearestOnly:
                        break

        self.log.debug('completed the ``_parse_the_ned_results`` method')
        return results, resultLen

    # use the tab-trigger below for new method
    def _parse_the_ned_object_results(
            self):
        """
        *parse the ned results*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::

            - @review: when complete, clean _parse_the_ned_results method
            - @review: when complete add logging
        """
        self.log.debug('starting the ``_parse_the_ned_results`` method')

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
            except IOError as e:
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
                    print(thisHeader)
                theseLines = str.split(matchObject.group(), '\n')
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
                        print(thisRow)

            else:
                for head in headers:
                    thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
                if not self.quiet:
                    print(thisRow)
        else:
            # Print the header for stdout
            thisHeader = "| "
            for head in headers:
                thisHeader += str(head).ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print(thisHeader)
            thisRow = "| "
            for head in headers:
                thisRow += str("").ljust(self.resultSpacing, ' ') + " | "
            if not self.quiet:
                print(thisRow)

        self.log.debug('completed the ``_parse_the_ned_results`` method')
        return results

        # use the tab-trigger below for new method
    def _convert_html_to_csv(
            self):
        """
        *contert html to csv*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::

            - @review: when complete, clean _convert_html_to_csv method
            - @review: when complete add logging
        """
        self.log.debug('starting the ``_convert_html_to_csv`` method')

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
            except IOError as e:
                message = 'could not open the file %s' % (pathToReadFile,)
                self.log.critical(message)
                raise IOError(message)
            except:
                if pathToReadFile == None:
                    message = 'we have no file to open'
                    self.log.error(message)
                    continue
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

        self.log.debug('completed the ``_convert_html_to_csv`` method')
        return None

    # use the tab-trigger below for new method
    def _parse_the_ned_list_results(
            self):
        """
        *parse the ned results*

        **Key Arguments**

        # -
        

        **Return**

        - None
        

        .. todo::

            - @review: when complete, clean _parse_the_ned_results method
            - @review: when complete add logging
        """
        self.log.debug('starting the ``_parse_the_ned_list_results`` method')

        results = []

        # CHOOSE VALUES TO RETURN
        allHeaders = ["searchIndex", "searchRa", "searchDec", "row_number", "input_note", "input_name", "ned_notes", "ned_name", "ra", "dec", "eb-v", "object_type", "redshift", "redshift_err", "redshift_quality", "magnitude_filter",
                      "major_diameter_arcmin", "minor_diameter_arcmin", "morphology", "hierarchy", "galaxy_morphology", "radio_morphology", "activity_type", "distance_indicator", "distance_mod", "distance"]
        if self.verbose == True:
            headers = ["searchIndex", "searchRa", "searchDec", "row_number", "input_note", "input_name", "ned_notes", "ned_name", "ra", "dec", "eb-v", "object_type", "redshift", "redshift_err", "redshift_quality", "magnitude_filter",
                       "major_diameter_arcmin", "minor_diameter_arcmin", "morphology", "hierarchy", "galaxy_morphology", "radio_morphology", "activity_type", "distance_indicator", "distance_mod", "distance"]
        else:
            headers = [
                "searchIndex", "searchRa", "searchDec", "ned_name", "ra", "dec", "object_type", "redshift"]

        if self.theseBatchParams == False:
            allHeaders = allHeaders[3:]
            headers = headers[3:]

        for thisFile in self.nedResults:
            if thisFile:
                pathToReadFile = thisFile
                # FIND THE BATCH INDEX NUMBER
                thisIndex = int(thisFile.split("/")[-1].split("_")[0])
                try:
                    self.log.debug("attempting to open the file %s" %
                                   (pathToReadFile,))
                    readFile = codecs.open(
                        pathToReadFile, encoding='utf-8', mode='rb')
                    thisData = readFile.read()
                    readFile.close()
                except IOError as e:
                    message = 'could not open the file %s' % (pathToReadFile,)
                    self.log.critical(message)
                    raise IOError(message)
                readFile.close()

                # GRAB THE ROWS OF DATA
                matchObject = re.search(
                    r"\n1\s*?\|\s*?.*", thisData, re.S)
                thisRow = ""
                if matchObject:
                    thisHeader = ""
                    for head in allHeaders:
                        thisHeader += str(head).ljust(self.resultSpacing,
                                                      ' ') + " | "
                    theseLines = str.split(matchObject.group(), '\n')[1:]

                    if self.theseBatchParams:
                        newLines = []
                        for t, b in zip(theseLines, self.theseBatchParams[thisIndex]):
                            t = "%s | %s | %s | %s " % (
                                b["searchIndex"], b["searchRa"], b["searchDec"], t)
                            newLines.append(t)
                        theseLines = newLines

                    theseLines = [thisHeader] + theseLines
                    csvReader = csv.DictReader(
                        theseLines, dialect='excel', delimiter='|', quotechar='"')
                    for row in csvReader:
                        thisDict = {}
                        row = dict(row)
                        if not list(row.keys()):
                            continue
                        if None in list(row.keys()):
                            continue
                        if "ned_name" not in ("").join(list(row.keys())).lower():
                            continue
                        for k, v in list(row.items()):
                            try:
                                # self.log.debug("attempting to strip ned key")
                                k = k.strip()
                            except Exception as e:
                                self.log.error(
                                    'cound not strip ned key (%(k)s, %(v)s)' % locals())
                                self.log.error(
                                    "could not strip ned key - failed with this error: %s " % (str(e),))
                                break
                            if (k == "ra" or k == "dec"):
                                v = v.replace("h", ":").replace(
                                    "m", ":").replace("d", ":").replace("s", "")
                            if isinstance(v, ("".__class__, u"".__class__)):
                                v = v.strip()
                            thisDict[k] = v
                        results.append(thisDict)

                os.remove(thisFile)

        self.log.debug('completed the ``_parse_the_ned_list_results`` method')
        return results, headers

    def _split_incoming_queries_into_batches(
            self,
            sources,
            searchParams=False):
        """
        *split incoming queries into batches*

        **Key Arguments**

        - ``sources`` -- sources to split into batches
        - ``searchParams`` -- search params associated with batches
        

        **Return**

        - ``theseBatches`` -- list of batches
        - ``theseBatchParams`` -- params associated with batches
        
        """
        self.log.debug(
            'completed the ````_split_incoming_queries_into_batches`` method')

        batchSize = 180
        total = len(sources)
        batches = int(old_div(total, batchSize)) + 1

        start = 0
        end = 0
        theseBatches = []
        theseBatchParams = []
        for i in range(batches):
            end = end + batchSize
            start = i * batchSize
            thisBatch = sources[start:end]
            theseBatches.append(thisBatch)

            if searchParams != False:
                thisBatch = searchParams[start:end]
                theseBatchParams.append(thisBatch)

        if len(theseBatchParams) == 0:
            theseBatchParams = False

        self.log.debug(
            'completed the ``_split_incoming_queries_into_batches`` method')
        return theseBatches, theseBatchParams

        # use the tab-trigger below for new method
        # xt-class-method
