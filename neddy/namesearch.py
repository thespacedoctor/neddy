#!/usr/local/bin/python
# encoding: utf-8
"""
namesearch.py
=============
:Summary:
    A Name Searcher for NED

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
import urllib
from docopt import docopt
from dryxPython import webcrawlers as dwc
from dryxPython import logs as dl
from dryxPython import commonutils as dcu
from dryxPython.projectsetup import setup_main_clutil
from neddy import _basesearch

###################################################################
# CLASSES                                                         #
###################################################################


class namesearch(_basesearch):

    """
    The worker class for the namesearch module

    **Key Arguments:**
        - ``log`` -- logger
        - ``name`` -- name
        - ``quiet`` -- don't print to stdout


    **Todo**
        - @review: when complete, clean namesearch class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            names,
            quiet=False
    ):
        self.log = log
        log.debug("instantiating a new 'namesearch' object")
        self.names = names
        self.quiet = quiet

        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes
        self.resultSpacing = 20

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions
        os.environ['TERM'] = 'vt100'
        if not isinstance(self.names, list):
            self.uplist = [self.names]
        else:
            self.uplist = self.names

        return None

    def close(self):
        del self
        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """get the namesearch object

        **Return:**
            - ``namesearch``

        **Todo**
            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        self.theseBatches = self._split_incoming_queries_into_batches(
            sources=self.uplist)
        self._build_api_url_and_download_results()
        results = self._parse_the_ned_list_results()

        self.log.info('completed the ``get`` method')
        return results

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

        baseUrl = "https://ned.ipac.caltech.edu/cgi-bin/"
        command = "gmd"
        uplist = self.uplist  # note newline `%0D%0`
        urlParameters = {
            "delimiter": "bar",
            "NO_LINKS": "1",
            "nondb": ["row_count", "user_name_msg", "user_objname"],
            "crosid": "objname",
            "enotes": "objnote",
            "position": ["ra,dec", "bhextin", "pretype", "z", "zunc", "zflag"],
            "gadata": ["magnit", "sizemaj", "sizemin", "morphol"],
            "attdat_CON": ["M", "S", "H", "R", "z"],
            "distance_CON": ["mm", "dmpc"],
            "attdat": "attned"
        }

        queryBase = "%(baseUrl)s%(command)s?uplist=" % locals()
        queryList = []

        for batch in self.theseBatches:
            thisLength = len(batch)
            queryUrl = queryBase
            for thisIndex, thisName in enumerate(batch):
                queryUrl = queryUrl + urllib.quote(thisName)
                if thisIndex < thisLength - 1:
                    queryUrl = queryUrl + "%0D"

            for k, v in urlParameters.iteritems():
                if isinstance(v, list):
                    for item in v:
                        queryUrl = queryUrl + "&" + \
                            k + "=" + urllib.quote(item)
                else:
                    queryUrl = queryUrl + "&" + k + "=" + urllib.quote(v)

            queryList.append(queryUrl)

        self.nedResults = dwc.multiWebDocumentDownloader(
            urlList=queryList,
            # directory(ies) to download the documents to - can be one url or a
            # list of urls the same length as urlList
            downloadDirectory="/tmp/",
            log=self.log,
            timeStamp=1,
            timeout=3600,
            concurrentDownloads=5,
            resetFilename=False,
            credentials=False,  # { 'username' : "...", "password", "..." }
            longTime=True
        )

        self._convert_html_to_csv()

        self.log.info(
            'completed the ``_build_api_url_and_download_results`` method')
        return None

    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
