#!/usr/local/bin/python
# encoding: utf-8
"""
*Get common file and folder paths for the host package*

:Author:
    David Young
"""
import sys
import os
from docopt import docopt

###################################################################
# CLASSES                                                         #
###################################################################

###################################################################
# PUBLIC FUNCTIONS                                                #
###################################################################
# LAST MODIFIED : October 24, 2013
# CREATED : October 24, 2013
# AUTHOR : DRYX

# copy usage method(s) here and select the following snippet from the command palette:
# x-setup-worker-function-parameters-from-usage-method

def getpackagepath():
    """
    *getpackagepath*

    **Key Arguments**

    - None
    

    **Return**

    - ``packagePath`` -- path to the host package
    

    .. todo::

        - when complete, clean worker function and add comments
        - when complete add logging
    """
    ## STANDARD LIB ##
    ## THIRD PARTY ##
    ## LOCAL APPLICATION ##

    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + "/../"

    return packagePath
###################################################################
# PRIVATE (HELPER) FUNCTIONS                                      #
###################################################################

############################################
# CODE TO BE DEPECIATED                    #
############################################

if __name__ == '__main__':
    main()

###################################################################
# TEMPLATE FUNCTIONS                                              #
###################################################################
