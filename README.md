# neddy

[![](https://zenodo.org/badge/DOI/10.5281/zenodo.8037632.svg)](https://zenodo.org/doi/10.5281/zenodo.8037632) 

<!-- INFO BADGES -->  

[![](https://img.shields.io/pypi/pyversions/neddy)](https://pypi.org/project/neddy/)
[![](https://img.shields.io/pypi/v/neddy)](https://pypi.org/project/neddy/)
[![](https://img.shields.io/conda/vn/conda-forge/neddy)](https://anaconda.org/conda-forge/neddy)
[![](https://pepy.tech/badge/neddy)](https://pepy.tech/project/neddy)
[![](https://img.shields.io/github/license/thespacedoctor/neddy)](https://github.com/thespacedoctor/neddy)

<!-- STATUS BADGES -->  

[![](https://soxs-eso-data.org/ci/buildStatus/icon?job=neddy%2Fmaster&subject=build%20master)](https://soxs-eso-data.org/ci/blue/organizations/jenkins/neddy/activity?branch=master)
[![](https://soxs-eso-data.org/ci/buildStatus/icon?job=neddy%2Fdevelop&subject=build%20dev)](https://soxs-eso-data.org/ci/blue/organizations/jenkins/neddy/activity?branch=develop)
[![](https://cdn.jsdelivr.net/gh/thespacedoctor/neddy@master/coverage.svg)](https://raw.githack.com/thespacedoctor/neddy/master/htmlcov/index.html)
[![](https://readthedocs.org/projects/neddy/badge/?version=master)](https://neddy.readthedocs.io/en/master/)
[![](https://img.shields.io/github/issues/thespacedoctor/neddy/type:%20bug?label=bug%20issues)](https://github.com/thespacedoctor/neddy/issues?q=is%3Aissue+is%3Aopen+label%3A%22type%3A+bug%22+)

*Query the Nasa Extra-Galactic (NED) database via the command-line and programmatically*.

Documentation for neddy is hosted by [Read the Docs](https://neddy.readthedocs.io/en/master/) ([development version](https://neddy.readthedocs.io/en/develop/) and [master version](https://neddy.readthedocs.io/en/master/)). The code lives on [github](https://github.com/thespacedoctor/neddy). Please report any issues you find [here](https://github.com/thespacedoctor/neddy/issues).

## Features

* A command-line suite to query NED for a given source name or via a sky-location conesearch.
* The ability to send multiple name or conesearch queries with a single command.
* Integrate neddy into your own python scripts to build your own workflows.

## Installation

The best way to install or upgrade neddy is to use `conda` to install the package in its own isolated environment, as shown here:

``` bash
conda create -n neddy python=3.9 neddy -c conda-forge
conda activate neddy
```

If you have previously installed neddy, a warning will be issued stating that a conda environment already exists; select 'y' when asked to remove the existing environment.

To check installation was successful run `neddy -v`. This should return the version number of the install.

## Initialisation 

Before using neddy you need to use the `init` command to generate a user settings file. Running the following creates a [yaml](https://learnxinyminutes.com/docs/yaml/) settings file in your home folder under `~/.config/neddy/neddy.yaml`:

```bash
neddy init
```

The file is initially populated with neddy's default settings which can be adjusted to your preference.

If at any point the user settings file becomes corrupted or you just want to start afresh, simply trash the `neddy.yaml` file and rerun `neddy init`.

## How to cite neddy

If you use `neddy` in your work, please cite using the following BibTeX entry: 

```bibtex
@software{Young_neddy,
    author = {Young, David R.},
    doi = {10.5281/zenodo.8037632},
    license = {GPL-3.0-only},
    title = {{neddy. Query the Nasa Extra-Galactic from the command-line}},
    url = {https://zenodo.org/doi/10.5281/zenodo.8037632}
}
```
 
