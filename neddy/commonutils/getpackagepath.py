#!/usr/local/bin/python
# encoding: utf-8
"""
*Get common file and folder paths for the neddy package*

:Author:
    David Young
"""


def getpackagepath():
    """
    *Return the root folder path for the neddy package*
    """
    import os

    moduleDirectory = os.path.dirname(__file__)
    packagePath = os.path.dirname(__file__) + "/../"

    return packagePath
