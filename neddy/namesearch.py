#!/usr/local/bin/python
# encoding: utf-8
"""
*A Name Searcher for NED*

:Author:
    David Young

:Date Created:
    May 6, 2015
"""
################# GLOBAL IMPORTS ####################
import sys
import os
import readline
import glob
import pickle
import urllib
from docopt import docopt
from fundamentals.download import multiobject_download
from fundamentals import tools, times
from neddy import _basesearch

###################################################################
# CLASSES                                                         #
###################################################################


class namesearch(_basesearch):

    """
    *The worker class for the namesearch module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``name`` -- name
        - ``quiet`` -- don't print to stdout
        - ``verbose`` -- return more metadata for matches
        - ``searchParams`` -- list of dictionaries to prepend to results
        - ``outputFilePath`` -- path to file to output results to
    """
    # Initialisation

    def __init__(
            self,
            log,
            names,
            quiet=False,
            verbose=False,
            searchParams=False,
            outputFilePath=False
    ):
        self.log = log
        log.debug("instantiating a new 'namesearch' object")
        self.names = names
        self.quiet = quiet
        self.verbose = verbose
        self.searchParams = searchParams
        self.outputFilePath = outputFilePath
        # xt-self-arg-tmpx

        # VARIABLE DATA ATRRIBUTES
        self.resultSpacing = 15

        # Initial Actions
        # CREATE A LIST IF SINGLE NAME GIVEN
        os.environ['TERM'] = 'vt100'
        if not isinstance(self.names, list):
            self.uplist = [self.names]
        else:
            self.uplist = self.names

        return None

    # METHOD ATTRIBUTES
    def get(self):
        """
        *get the namesearch object*

        **Return:**
            - ``results``
        """
        self.log.debug('starting the ``get`` method')

        # SPLIT THE LIST OF NAMES INTO BATCHES
        self.theseBatches, self.theseBatchParams = self._split_incoming_queries_into_batches(
            sources=self.uplist,
            searchParams=self.searchParams
        )

        # PERFORM NAME QUERIES AGAINST NED
        self._build_api_url_and_download_results()
        self.results, self.headers = self._parse_the_ned_list_results()
        self._output_results()

        self.log.debug('completed the ``get`` method')
        return self.results

    def _build_api_url_and_download_results(
            self):
        """
        *build api url for NED to perform batch name queries*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean _build_api_url_and_download_results method
            - @review: when complete add logging
        """
        self.log.debug(
            'completed the ````_build_api_url_and_download_results`` method')

        baseUrl = "https://ned.ipac.caltech.edu/cgi-bin/"
        command = "gmd"
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

        # BUILD THE LIST OF QUERIES
        for batch in self.theseBatches:
            thisLength = len(batch)
            queryUrl = queryBase
            # ADD NAMES
            for thisIndex, thisName in enumerate(batch):
                queryUrl = queryUrl + urllib.quote(thisName)
                if thisIndex < thisLength - 1:
                    queryUrl = queryUrl + "%0D"
            # ADD PARAMETERS
            for k, v in urlParameters.iteritems():
                if isinstance(v, list):
                    for item in v:
                        queryUrl = queryUrl + "&" + \
                            k + "=" + urllib.quote(item)
                else:
                    queryUrl = queryUrl + "&" + k + "=" + urllib.quote(v)
            queryList.append(queryUrl)

        # PULL THE RESULT PAGES FROM NED
        self.nedResults = multiobject_download(
            urlList=queryList,
            downloadDirectory="/tmp",
            log=self.log,
            timeStamp=1,
            timeout=3600,
            concurrentDownloads=10,
            resetFilename=False,
            credentials=False,  # { 'username' : "...", "password", "..." }
            longTime=True,
            indexFilenames=True
        )

        for thisIndex, r in enumerate(self.nedResults):
            if r == None:
                thisUrl = queryList[thisIndex]
                self.log.error(
                    'cound not download NED results for URL %(thisUrl)s' % locals())
                sys.exit(0)

        self._convert_html_to_csv()

        self.log.debug(
            'completed the ``_build_api_url_and_download_results`` method')
        return None

    def _output_results(
            self):
        """
        *output results*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean _output_results method
            - @review: when complete add logging
        """
        self.log.debug('starting the ``_output_results`` method')

        content = ""
        maxNameLen = 0

        for r in self.results:
            if maxNameLen < len(r["ned_name"]):
                maxNameLen = len(r["ned_name"])

        if len(self.results) == 0:
            content += "No resuls found"
        else:
            thisHeader = "| "
            thisLine = "| "
            for head in self.headers:
                if head == "ned_name":
                    s = maxNameLen
                else:
                    s = self.resultSpacing
                thisHeader += str(head).ljust(s,
                                              ' ') + " | "
                thisLine += ":".ljust(s,
                                      '-') + " | "
            content += thisHeader
            content += "\n" + thisLine
            for r in self.results:
                thisRow = "| "
                for head in self.headers:
                    if head == "ned_name":
                        s = maxNameLen
                    else:
                        s = self.resultSpacing
                    thisRow += str(r[head]).ljust(s,
                                                  ' ') + " | "
                content += "\n" + thisRow

        if self.quiet == False:
            print content
        if self.outputFilePath:
            import codecs
            writeFile = codecs.open(
                self.outputFilePath, encoding='utf-8', mode='w')
            writeFile.write(content)
            writeFile.close()

        self.log.debug('completed the ``_output_results`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx
