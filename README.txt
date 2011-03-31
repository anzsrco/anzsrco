
ANZSRC RDF ocnversion:
======================


This project contains a set of pythonscripts to generate ANZSRC ontologies.

BUILD:
======

First stop is to build the toolset. The build process is managed by
*buildout*. The build process automatically downloads all missing dependencies
and installs a set of of executable scripts in ``./bin``.

Commands to run::

  # initialise the build environment:
  python bootstrap.py
  # start the build process
  ./bin/buildout

Usage:
======

The original source data is acquired from the ABS Website and the csv files are
stored under ``./anzsrc_data``. The script ``./bin/genanzsrc`` uses this data
and generates a set of rdf files in ``./anzsrc_output``.


Generated Namespaces:
=====================

Todo: quiclky describe all namepsaces generated


Generated Files:
================

Todo: quickly describe the remainder of the generated files
