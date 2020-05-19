neddy 
=========================

*CL-util to query the NASA/IPAC Extragalactic Database (NED)*.

Usage
======

.. code-block:: bash 
   
    neddy [-nuvr] cone (filelist <pathToCoordinateList> <radiusArcsec> | <ra> <dec> <radiusArcsec>) [<outPutFile>]
    neddy [-v] obj <objectName> [<objectName>...]
    
    -h, --help            show this help message
    -n, --nearest         nearest object only
    -u, --unclassified    include unclassifed extra-galaxtic objects
    -v, --verbose         return more metadata for matches
    -r, --redshift        redshift must be available
    ra                    ra (decimal degrees or sexegesimal)
    dec                   dec (decimal degrees or sexegesimal)
    radiusArcsec          radiusArcsec (conesearch radius)
    objectName            objectName (the name of the object)
    pathToCoordinateList  path to list of ra dec radiusArcsec
    outPutFile            path to outputfile
    
Documentation
=============

Documentation for neddy is hosted by `Read the Docs <http://neddy.readthedocs.org/en/stable/>`__ (last `stable version <http://neddy.readthedocs.org/en/stable/>`__ and `latest version <http://neddy.readthedocs.org/en/latest/>`__).

Installation
============

The easiest way to install neddy is to use ``pip``:

.. code:: bash

    pip install neddy

Or you can clone the `github repo <https://github.com/thespacedoctor/neddy>`__ and install from a local version of the code:

.. code:: bash

    git clone git@github.com:thespacedoctor/neddy.git
    cd neddy
    python setup.py install

To upgrade to the latest version of neddy use the command:

.. code:: bash

    pip install neddy --upgrade


Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

.. code:: bash

    git clone git@github.com:thespacedoctor/neddy.git
    cd neddy
    python setup.py develop

`Pull requests <https://github.com/thespacedoctor/neddy/pulls>`__
are welcomed!


Issues
------

Please report any issues
`here <https://github.com/thespacedoctor/neddy/issues>`__.

License
=======

Copyright (c) 2018 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

