#!/usr/local/bin/python
# encoding: utf-8
"""
conesearch.py
=============
:Summary:
    Perform a conesearch on NED

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
import readline
import glob
import pickle
import codecs
import re
import string
import csv
from docopt import docopt
from dryxPython import webcrawlers as dwc
from dryxPython import astrotools as dat
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
# from ..__init__ import *


###################################################################
# CLASSES                                                         #
###################################################################
class conesearch():

    """
    The worker class for the conesearch module

    **Key Arguments:**
        - ``log`` -- logger
        - ``ra`` -- ra
        - ``dec`` -- dec
        - ``radiusArcsec`` -- radiusArcsec
        - ``nearestOnly`` -- return only the nearest object from NED
        - ``unclassified`` -- include the unclassified sources in the return results

    **Todo**
        - @review: when complete, clean conesearch class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
        self,
        log,
        ra,
        dec,
        radiusArcsec,
        nearestOnly=False,
        unclassified=False
    ):
        self.log = log
        self.log.debug("instansiating a new 'conesearch' object")
        self.ra = ra
        self.dec = dec
        self.arcsec = radiusArcsec
        self.nearestOnly = nearestOnly
        self.unclassified = unclassified

        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes
        self.arcmin = float(self.arcsec) / 60.

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions
        self._convert_coordinates_to_decimal_degrees()

        return None

    def close(self):
        del self
        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """get the conesearch object

        **Return:**
            - ``conesearch``

        **Todo**
            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        self._build_api_url_and_download_results()
        self._parse_the_ned_results()
        print self.__dict__

        self.log.info('completed the ``get`` method')
        return conesearch

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
    def _build_api_url_and_download_results(
            self):
        """ build api url for NED

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _build_api_url_and_download_results method
            - @review: when complete add logging
        """
        self.log.info(
            'starting the ``_build_api_url_and_download_results`` method')

        raDeg = self.raDeg
        decDeg = self.decDeg
        arcmin = self.arcmin

        if self.unclassified:
            url = "http://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon=%(raDeg)sd&lat=%(decDeg)sd&radius=%(arcmin)s&&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes1=GPairs&in_objtypes1=GTriples&in_objtypes1=GGroups&in_objtypes1=GClusters&in_objtypes1=QSO&in_objtypes1=QSOGroups&in_objtypes1=GravLens&in_objtypes1=AbsLineSys&in_objtypes1=EmissnLine&in_objtypes2=Radio&in_objtypes2=SmmS&in_objtypes2=Infrared&in_objtypes2=Visual&in_objtypes2=UvSource&in_objtypes2=UVExcess&in_objtypes2=Xray&in_objtypes2=GammaRay&search_type=Near+Position+Search&nmp_op=ANY&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES&of=ascii_bar" % locals(
            )
        else:
            url = "http://ned.ipac.caltech.edu/cgi-bin/objsearch?search_type=Near+Position+Search&in_csys=Equatorial&in_equinox=J2000.0&lon=%(raDeg)sd&lat=%(decDeg)sd&radius=%(arcmin)s&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&z_constraint=Unconstrained&z_value1=&z_value2=&z_unit=z&ot_include=ANY&in_objtypes1=Galaxies&in_objtypes1=GPairs&in_objtypes1=GTriples&in_objtypes1=GGroups&in_objtypes1=GClusters&in_objtypes1=QSO&in_objtypes1=QSOGroups&in_objtypes1=GravLens&in_objtypes1=AbsLineSys&in_objtypes1=EmissnLine&nmp_op=ANY&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=Distance+to+search+center&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES&of=ascii_bar" % locals(
            )

        self.nedResults = dwc.singleWebDocumentDownloader(
            url=url,
            downloadDirectory="/tmp",
            log=self.log,
            timeStamp=1,
            credentials=False
        )

        self.log.info(
            'completed the ``_build_api_url_and_download_results`` method')
        return None

    # use the tab-trigger below for new method
    def _parse_the_ned_results(
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
                    thisHeader += str(head).ljust(40, ' ') + " | "
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
                        thisRow += str(thisDict[head]).ljust(40, ' ') + " | "
                    print thisRow
                    if self.nearestOnly:
                        break
            else:
                for head in headers:
                    thisRow += str("").ljust(40, ' ') + " | "
                print thisRow
        else:
            # Print the header for stdout
            thisHeader = "| "
            for head in headers:
                thisHeader += str(head).ljust(40, ' ') + " | "
            print thisHeader
            thisRow = "| "
            for head in headers:
                thisRow += str("").ljust(40, ' ') + " | "
            print thisRow

        self.log.info('completed the ``_parse_the_ned_results`` method')
        return results

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx


if __name__ == '__main__':
    main()
