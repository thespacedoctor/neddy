#!/usr/local/bin/python
# encoding: utf-8
"""
*Perform a conesearch on NED*

:Author:
    David Young
"""
from __future__ import print_function
from __future__ import division
from neddy import _basesearch
import os
import sys
from future import standard_library
standard_library.install_aliases()
os.environ['TERM'] = 'vt100'


class conesearch(_basesearch):
    """
    *The NED conesearch object*

    **Key Arguments**

    - ``log`` -- logger
    - ``ra`` -- ra
    - ``dec`` -- dec
    - ``radiusArcsec`` -- the search radius in arcsecs
    - ``nearestOnly`` -- return only the nearest object from NED
    - ``unclassified`` -- include the unclassified sources in the search results
    - ``quiet`` -- don't print to stdout
    - ``listOfCoordinates`` -- a list of `ra`, `dec`, and `radiusArcsec` (multiple sources)
    - ``outputFilePath`` -- path of file to print results to. Default *False* (don't print to file)
    - ``verbose`` -- return more metadata for matches
    - ``redshift`` -- require a redshift for a source to appear in search results

    **Usage**

    ```python
    from neddy import conesearch
    search = conesearch(
        log=log,
        ra=0.000,
        dec=0.000,
        radiusArcsec=5.0,
        nearestOnly=False,
        unclassified=True,
        outputFilePath=False,
        verbose=True,
        redshift=False
    )
    results = search.get()
    ```
    """

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

        # VARIABLE DATA ATRRIBUTES
        from past.utils import old_div
        self.arcmin = old_div(float(self.arcsec), 60.)
        self.resultSpacing = 30

        # CREATE A LIST IF SINGLE COORDINATES GIVEN
        if self.listOfCoordinates == False:
            self.listOfCoordinates = ["%(ra)s %(dec)s" % locals()]
        self._convert_coordinates_to_decimal_degrees()

        return None

    def get(self):
        """
        *return results of a NED conesearch*
        """
        self.log.debug('starting the ``get`` method')
        from neddy import namesearch

        # SEARCH NED WITH SINGLE CONESEARCHES TO RETURN LIST OF MATCHED NAMES
        names, searchParams = self.get_crossmatch_names(
            listOfCoordinates=self.listOfCoordinates,
            radiusArcsec=self.arcsec
        )

        # NOW PERFORM A NAME SEARCH AGAINST THE MATCHED NAMES
        search = namesearch(
            log=self.log,
            names=names,
            quiet=False,
            searchParams=searchParams,
            verbose=self.verbose,
            outputFilePath=self.outputFilePath
        )
        results = search.get()

        self.log.debug('completed the ``get`` method')
        return results

    def _get_ned_query_url(
            self,
            raDeg,
            decDeg,
            arcsec):
        """
        *build and return the NED conesearch URL for a single coordinate*

        **Key Arguments**

        - ``raDeg`` -- conesearch centre RA
        - ``decDeg`` -- conesearch centre DEC
        - ``arcsec`` -- conesearch radius in arcsec

        **Return**

        - ``url`` -- the conesearch URL
        """
        self.log.debug('starting the ``_get_ned_query_url`` method')

        import urllib.parse
        from past.utils import old_div

        radArcMin = old_div(float(arcsec), (60.))

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

        url = url + "?" + urllib.parse.urlencode(params)
        if not self.unclassified:
            url = url + "&" + urllib.parse.urlencode({"ot_include": "ANY"})
            in_objtypes1 = ["Galaxies", "GPairs", "GTriples", "GGroups",
                            "GClusters", "QSO", "QSOGroups", "GravLens", "AbsLineSys", "EmissnLine"]
            for o in in_objtypes1:
                url = url + "&" + urllib.parse.urlencode({"in_objtypes1": o})
            in_objtypes3 = ["Supernovae", "HIIregion", "PN", "SNR", "StarAssoc", "StarClust", "MolCloud", "Nova", "VarStar", "WolfRayet",
                            "CarbonStar", "PofG", "Other", "Star", "BlueStar", "RedStar", "Pulsar", "ReflNeb", "DblStar", "EmissnObj", "EmissnNeb", "WhiteDwarf"]
            for o in in_objtypes3:
                url = url + "&" + urllib.parse.urlencode({"in_objtypes3": o})

        self.log.debug('completed the ``_get_ned_query_url`` method')
        return url

    def get_crossmatch_names(
            self,
            listOfCoordinates=False,
            radiusArcsec=False):
        """
        *return a list of NED sources found within the conesearch radius*

        **Key Arguments**

        - ``listOfCoordinates`` -- list of the coordinates to conesearch
        - ``radiusArcsec`` -- the search radius

        **Return**

        - ``names`` -- the names of the sources matched within the search radius
        - ``searchParams`` -- the parameters of the search as read from the command-line/method call
        """
        self.log.debug('starting the ``get_crossmatch_names`` method')

        from fundamentals.download import multiobject_download

        if listOfCoordinates == False:
            listOfCoordinates = self.listOfCoordinates
        if radiusArcsec == False:
            radiusArcsec = self.arcsec

        names = []
        searchParams = []
        nedUrls = []

        # GENERATE NED CONESEARCH URLS
        for i, coord in enumerate(listOfCoordinates):
            url = self._get_ned_query_url(
                raDeg=coord[0],
                decDeg=coord[1],
                arcsec=radiusArcsec
            )
            nedUrls.append(url)

        count = len(nedUrls)
        if count:
            print(f"{count} NED conesearch URLs have been built. Requesting from NED ...")

        # DOWNLOAD THE RESULTS TO FILE
        localUrls = multiobject_download(
            urlList=nedUrls,
            downloadDirectory="/tmp",
            log=self.log,
            timeStamp=True,
            timeout=3600,
            concurrentDownloads=10,
            resetFilename=False,
            credentials=False,  # { 'username' : "...", "password", "..." }
            longTime=True,
            indexFilenames=True
        )

        count = len(localUrls)
        if count:
            print(f"{count} conesearch results downloaded from NED")

        for ii, nedResults in enumerate(localUrls):
            if nedResults == None:
                thisUrl = nedUrls[ii]
                self.log.error(
                    f'cound not download results for NED URL: {thisUrl}')
                continue
            i = int(nedResults.split("/")[-1].split("_")[0])

            # PARSE CONESEARCH RESULTS INTO PYTHON DICTS
            results, resultLen = self._parse_the_ned_position_results(
                ra=listOfCoordinates[i][0],
                dec=listOfCoordinates[i][1],
                nedResults=nedResults
            )
            print(f"  {resultLen} returned from single NED conesearch")
            if resultLen > 45000:
                print(" To many results returned from single NED query ... aborting!")

                # DO FINER SUB-SEARCHES TO COLLECT ALL NED MATCH RESULTS
                subnames, subsearchParams = self._oversized_subqueries(
                    coordinate=listOfCoordinates[i],
                    radiusArcsec=radiusArcsec
                )
                names += subnames
                searchParams += subsearchParams
            else:
                for r in results:
                    searchParams.append(
                        {"searchIndex": i + 1, "searchRa": r["searchRa"], "searchDec": r["searchDec"]})
                    names.append(r["matchName"])
            os.remove(nedResults)

        self.log.debug('completed the ``get_crossmatch_names`` method')
        return names, searchParams

    def _oversized_subqueries(
            self,
            coordinate,
            radiusArcsec):
        """
        *subdivide an oversized query (> 50,000 matches in NED get truncated to 50000) into finer search areas*

        **Key Arguments**

        - ``coordinate`` -- the crowd-field RA and DEC. 
        - ``radiusArcsec`` -- the original search radius

        **Return**

        - ``names`` -- the matched names
        - ``searchParams`` -- the new search parameters
        """
        self.log.debug('starting the ``_oversized_subqueries`` method')

        import math
        from past.utils import old_div

        smallerRadiusArcsec = old_div(radiusArcsec, 2.)
        print("Calculating 7 sub-disks for coordinates %(coordinate)s, with smaller search radius of %(smallerRadiusArcsec)s arcsec" % locals())

        ra = coordinate[0]
        dec = coordinate[1]

        shifts = [
            (0, 0),
            (0, old_div(math.sqrt(3.), 2.)),
            (old_div(3., 4.), old_div(math.sqrt(3.), 4.)),
            (old_div(3., 4.), old_div(-math.sqrt(3.), 4.)),
            (0, old_div(-math.sqrt(3.), 2.)),
            (old_div(-3., 4.), old_div(-math.sqrt(3.), 4.)),
            (old_div(-3., 4.), old_div(math.sqrt(3.), 4.))
        ]

        subDiskCoordinates = []
        count = 0
        for s in shifts:
            x1 = ra + s[0] * radiusArcsec / (60 * 60)
            y1 = dec + s[1] * radiusArcsec / (60 * 60)
            subDiskCoordinates.append((x1, y1))

        names, searchParams = self.get_crossmatch_names(
            listOfCoordinates=subDiskCoordinates,
            radiusArcsec=smallerRadiusArcsec
        )

        self.log.debug('completed the ``_oversized_subqueries`` method')
        return names, searchParams


if __name__ == '__main__':
    main()
