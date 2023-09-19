#!/usr/local/bin/python
# encoding: utf-8
"""
*Perform a NED name-search and return the metadata for the matched sources*

:Author:
    David Young
"""
from __future__ import print_function
from neddy import _basesearch
import os
import sys
from future import standard_library
standard_library.install_aliases()


class namesearch(_basesearch):
    """
    *Perform a NED name-search and return the metadata for the matched sources*

    **Key Arguments**

    - ``log`` -- logger
    - ``name`` -- name
    - ``quiet`` -- don't print to stdout
    - ``verbose`` -- return more metadata for matches
    - ``searchParams`` -- list of dictionaries to prepend to results
    - ``outputFilePath`` -- path to file to output results to

    **Usage**

    ```python
    from neddy import namesearch
    search = namesearch(
        log=log,
        names=objectName,
        verbose=True,
        outputFilePath="/path/to/output.csv"
    )
    results = search.get()
    ```

    """

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

        # CREATE A LIST IF SINGLE NAME GIVEN
        os.environ['TERM'] = 'vt100'
        if not isinstance(self.names, list):
            self.uplist = [self.names]
        else:
            self.uplist = self.names

        return None

    def get(self):
        """
        *perform NED name searches and return the results*

        **Return**

        - ``results`` -- the search results (list of dictionaries)
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
        *build an API URL call for NED to perform batch name queries and download results*
        """
        self.log.debug(
            'completed the ````_build_api_url_and_download_results`` method')

        import urllib.parse
        from fundamentals.download import multiobject_download

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
                queryUrl = queryUrl + urllib.parse.quote(thisName)
                if thisIndex < thisLength - 1:
                    queryUrl = queryUrl + "%0D"
            # ADD PARAMETERS
            for k, v in list(urlParameters.items()):
                if isinstance(v, list):
                    for item in v:
                        queryUrl = queryUrl + "&" + \
                            k + "=" + urllib.parse.quote(item)
                else:
                    queryUrl = queryUrl + "&" + k + "=" + urllib.parse.quote(v)
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
        *print the NED search results to STDOUT and/or an output file*
        """
        self.log.debug('starting the ``_output_results`` method')

        from fundamentals.renderer import list_of_dictionaries

        if len(self.results) == 0:
            content = "No resuls found"
            csvContent = "No resuls found"
        else:
            dataSet = list_of_dictionaries(
                log=self.log,
                listOfDictionaries=self.results,
            )
            content = dataSet.table(filepath=None)
            if self.outputFilePath:
                csvContent = dataSet.csv(filepath=self.outputFilePath)

        if self.quiet == False:
            print(content)

        self.log.debug('completed the ``_output_results`` method')
        return None
