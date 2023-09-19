
## Command-line Usage

Here is neddy's entire CLI usage. More detail on each command can be found elsewhere in the docs.

```bash 


Usage:
    neddy init
    neddy [-nuvr] cone <ra> <dec> <radiusArcsec> [--o <outputFile>]
    neddy [-nuvr] cones <pathToCoordinateList> <radiusArcsec> [--o <outputFile>]
    neddy [-v] name <objectName> [<objectName>...] [--o <outputFile>]

Commands:    
    init                  initialise neddy for the first time
    cone                  perform a single conesearch on NED and return any matches
    cones                 perform bulk conesearches on NED and return any matches
    name                  perform name search(es) on NED and return any matches

Arguments:
    ra                    ra (decimal degrees or sexegesimal)
    dec                   dec (decimal degrees or sexegesimal)
    radiusArcsec          radiusArcsec (conesearch radius)
    objectName            objectName (the name of the object)
    pathToCoordinateList  path to list of space separated ra & dec (one coordinate set per line, decimal degrees or sexegesimal)
    --o outputFile        path to outputFile 
    
Options:
    -h, --help            show this help message
    -n, --nearest         return the nearest object only
    -u, --unclassified    include unclassified extra-galactic objects
    -v, --verbose         return more metadata for matches
    -r, --redshift        redshift must be available


```
