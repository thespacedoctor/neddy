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
        - ``listOfCoordinates`` -- list Of Coordinates ra dec radiusArcsec
        - ``outputFilePath`` -- path to output file
        - ``verbose`` -- return more metadata for matches

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
        verbose=False
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
        # xt-self-arg-tmpx

        # VARIABLE DATA ATRRIBUTES
        self.arcmin = float(self.arcsec) / 60.
        self.resultSpacing = 30

        # Initial Actions
        # CREATE A LIST IF SINGLE COORDINATES GIVEN
        if not self.listOfCoordinates:
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
        names, searchParams = self._get_crossmatch_names()

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
    def _single_ned_conesearch(
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
            - @review: when complete, clean _single_ned_conesearch method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_single_ned_conesearch`` method')

        radArcMin = float(arcsec) / (60.)

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
            "z_constraint": "Unconstrained",
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

        self.nedResults = dwc.singleWebDocumentDownloader(
            url=url,
            downloadDirectory="/tmp",
            log=self.log,
            timeStamp=1,
            credentials=False
        )

        results = self._parse_the_ned_position_results(
            ra=raDeg,
            dec=decDeg
        )

        self.log.info('completed the ``_single_ned_conesearch`` method')
        return results

    # use the tab-trigger below for new method
    def _get_crossmatch_names(
            self):
        """ get corssmatch names

        **Key Arguments:**
            # -

        **Return:**
            - None

        **Todo**
            - @review: when complete, clean _get_crossmatch_names method
            - @review: when complete add logging
        """
        self.log.info('starting the ``_get_crossmatch_names`` method')

        names = []
        searchParams = []
        for i, coord in enumerate(self.listOfCoordinates):
            results = self._single_ned_conesearch(
                raDeg=coord[0],
                decDeg=coord[1],
                arcsec=self.arcsec
            )

            for r in results:
                searchParams.append(
                    {"searchIndex": i + 1, "searchRa": r["searchRa"], "searchDec": r["searchDec"]})
                names.append(r["matchName"])

        self.log.info('completed the ``_get_crossmatch_names`` method')
        return names, searchParams

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx


if __name__ == '__main__':
    main()
