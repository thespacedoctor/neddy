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
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
import urllib
from docopt import docopt
from dryxPython import webcrawlers as dwc
from dryxPython import astrotools as dat
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
from neddy import _basesearch
from neddy import namesearch
# from ..__init__ import *


###################################################################
# CLASSES                                                         #
###################################################################
class conesearch(_basesearch):

    """
    The worker class for the conesearch module

    **Key Arguments:**
        - ``log`` -- logger
        - ``ra`` -- ra
        - ``dec`` -- dec
        - ``radiusArcsec`` -- radiusArcsec
        - ``nearestOnly`` -- return only the nearest object from NED
        - ``unclassified`` -- include the unclassified sources in the return results
        - ``quiet`` -- don't print to stdout
        - ``listOfCoordinates`` -- list of coordinates ra dec radiusArcsec
        - ``outputFilePath`` -- path to output file
        - ``verbose`` -- return more metadata for matches
        - ``redshift`` -- redshift constraint

    **Todo**
        - @review: when complete, clean conesearch class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation

    def __init__(
        self,
        log,
        ra=False,
        dec=False,
        radiusArcsec=False,
        nearestOnly=False,
        unclassified=False,
        quiet=False,
        listOfCoordinates=False,
        outputFilePath=False,
        verbose=False,
        redshift=False
    ):
        self.log = log
        self.log.debug("instansiating a new 'conesearch' object")
        self.ra = ra
        self.dec = dec
        self.arcsec = radiusArcsec
        self.nearestOnly = nearestOnly
        self.unclassified = unclassified
        self.quiet = quiet
        self.listOfCoordinates = listOfCoordinates
        self.outputFilePath = outputFilePath
        self.verbose = verbose
        self.redshift = redshift

        # xt-self-arg-tmpx

        # VARIABLE DATA ATRRIBUTES
        self.arcmin = float(self.arcsec) / 60.
        self.resultSpacing = 30

        # Initial Actions
        # CREATE A LIST IF SINGLE COORDINATES GIVEN
        if self.listOfCoordinates == False:
            self.listOfCoordinates = [ra + " " + dec]
        self._convert_coordinates_to_decimal_degrees()

        return None

    # METHOD ATTRIBUTES
    def get(self):
        """get the conesearch object

        **Return:**
            - ``conesearch``

        **Todo**
            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        # SEARCH NED WITH SINGLE CONESEARCHES TO RETURN LIST OF MATCHED NAMES
        names, searchParams = self.get_crossmatch_names()

        # NOW PERFORM A NAME SEARCH AGAINST THE MATCHED NAMES
        search = namesearch.namesearch(
            log=self.log,
            names=names,
            quiet=False,
            searchParams=searchParams,
            verbose=self.verbose,
            outputFilePath=self.outputFilePath
        )
        search.get()

        self.log.info('completed the ``get`` method')
        return conesearch

    # use the tab-trigger below for new method
    def _get_ned_query_url(
            self,
            raDeg,
            decDeg,
            arcsec):
        """ single ned conesearch

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _get_ned_query_url method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_get_ned_query_url`` method')

        radArcMin = float(arcsec) / (60.)

        if self.redshift == True:
            z_constraint = "Available"
        else:
            z_constraint = "Unconstrained"

        url = "http://ned.ipac.caltech.edu/cgi-bin/objsearch"
        params = {
            "in_csys": "Equatorial",
            "in_equinox": "J2000.0",
            "lon": "%(raDeg)0.6fd" % locals(),
            "lat": "%(decDeg)0.6fd" % locals(),
            "radius": "%(radArcMin)0.6s" % locals(),
            "hconst": "73",
            "omegam": "0.27",
            "omegav": "0.73",
            "corr_z": "1",
            "z_constraint": z_constraint,
            "z_value1": "",
            "z_value2": "",
            "z_unit": "z",
            "ot_include": "ANY",
            "nmp_op": "ANY",
            "out_csys": "Equatorial",
            "out_equinox": "J2000.0",
            "obj_sort": "Distance to search center",
            "of": "ascii_bar",
            "zv_breaker": "30000.0",
            "list_limit": "500",
            "img_stamp": "NO",
            "search_type": "Near Position Search",

        }

        url = url + "?" + urllib.urlencode(params)
        if not self.unclassified:
            url = url + "&" + urllib.urlencode({"ot_include": "ANY"})
            in_objtypes1 = ["Galaxies", "GPairs", "GTriples", "GGroups",
                            "GClusters", "QSO", "QSOGroups", "GravLens", "AbsLineSys", "EmissnLine"]
            for o in in_objtypes1:
                url = url + "&" + urllib.urlencode({"in_objtypes1": o})
            in_objtypes3 = ["Supernovae", "HIIregion", "PN", "SNR", "StarAssoc", "StarClust", "MolCloud", "Nova", "VarStar", "WolfRayet",
                            "CarbonStar", "PofG", "Other", "Star", "BlueStar", "RedStar", "Pulsar", "ReflNeb", "DblStar", "EmissnObj", "EmissnNeb", "WhiteDwarf"]
            for o in in_objtypes3:
                url = url + "&" + urllib.urlencode({"in_objtypes3": o})

        self.log.info('completed the ``_get_ned_query_url`` method')
        return url

    # use the tab-trigger below for new method
    def get_crossmatch_names(
            self):
        """ get corssmatch names

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean get_crossmatch_names method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get_crossmatch_names`` method')

        names = []
        searchParams = []
        nedUrls = []
        for i, coord in enumerate(self.listOfCoordinates):
            url = self._get_ned_query_url(
                raDeg=coord[0],
                decDeg=coord[1],
                arcsec=self.arcsec
            )
            nedUrls.append(url)

        count = len(nedUrls)
        if count:
            print "%(count)s NED conesearch URLs have been built. Requesting from NED ..." % locals()

        localUrls = dwc.multiWebDocumentDownloader(
            urlList=nedUrls,
            # directory(ies) to download the documents to - can be one url or a
            # list of urls the same length as urlList
            downloadDirectory="/tmp/",
            log=self.log,
            timeout=3600,
            concurrentDownloads=10,
            indexFilenames=True
        )

        count = len(localUrls)
        if count:
            print "%(count)s conesearch results downloaded from NED" % locals()

        for ii, self.nedResults in enumerate(localUrls):
            if self.nedResults == None:
                thisUrl = nedUrls[ii]
                self.log.error(
                    'cound not download results for NED URL: %(thisUrl)s' % locals())
                sys.exit(0)
            i = int(self.nedResults.split("/")[-1].split("_")[0])
            results, resultLen = self._parse_the_ned_position_results(
                ra=self.listOfCoordinates[i][0],
                dec=self.listOfCoordinates[i][1]
            )
            print "  %(resultLen)s returned from single NED conesearch" % locals()
            if resultLen > 45000:
                print " To many results returned from single NED query ... aborting!"
                sys.exit(0)
            for r in results:
                searchParams.append(
                    {"searchIndex": i + 1, "searchRa": r["searchRa"], "searchDec": r["searchDec"]})
                names.append(r["matchName"])

        self.log.info('completed the ``get_crossmatch_names`` method')
        return names, searchParams

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx


if __name__ == '__main__':
    main()
