Policy Options for Digital Infrastructure Strategies
====================================================
[![Build Status](https://travis-ci.org/edwardoughton/podis.svg?branch=master)](https://travis-ci.org/edwardoughton/podis)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/podis/badge.svg?branch=master)](https://coveralls.io/github/edwardoughton/podis?branch=master)

**podis** allows transparent and reproducible analysis of policies options for improving
digital infrastructure access, thus contributing to sustainable economic development.

The simulation model available in this repository can be applied to local, national or regional
telecommunication markets, to quantify the performance of different technology, business model
or regional integration options. The evidence produced can be used to inform the design of
digital infrastructure strategies.

Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called podis:

    conda create --name podis python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate podis

First, install optional packages:

    conda install geopandas rasterio rasterstats

Then install podis:

    python setup.py install

Alternatively, for development purposes, clone this repo and run:

    python setup.py develop


Download necessary data
=======================

You will need numerous input data sets.

First, download the Global Administrative Database (GADM), following the link below and making
sure you download the "six separate layers.":

- https://gadm.org/download_world.html

Place the data into the following path `data/raw/gadm36_levels_shp`.

Then download the WorldPop global settlement data from:

- https://www.worldpop.org/geodata/summary?id=24777.

Place the data in `data/raw/settlement_layer`.

Next, download the nightlight data here:

https://ngdc.noaa.gov/eog/data/web_data/v4composites/F182013.v4.tar

Place the unzipped data in `data/raw/nightlights/2013`.

Obtain the Mobile Coverage Explorer data from Collins Bartholomew:

https://www.collinsbartholomew.com/mobile-coverage-maps/mobile-coverage-explorer/

Place the data into `data/raw/Mobile Coverage Explorer`.

Once complete, run the following to preprocess all data:

    python scripts/preprocess.py


Using the model
===============

First run the following initial preprocessing script to extract the necessary files:

    python scripts/preprocess.py

Then

    python scripts/core.py


Thanks for the support
======================

**podis** was written and developed at the `Environmental Change Institute, University of Oxford <http://www.eci.ox.ac.uk>`_ within the EPSRC-sponsored MISTRAL programme, as part of the `Infrastructure Transition Research Consortium <http://www.itrc.org.uk/>`_.
