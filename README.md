.. -*- mode: rst -*-

=======================================
VLBI Imaging Script
=======================================

.. image:: https://img.shields.io/badge/license-%20GNU%20GPLv3-blue.svg?style=flat
        :target: https://github.com/rstofi/VLBI_Imaging_Script/blob/master/LICENSE

Python module for imaging VLBI data based on *difmap*. It contains a growing library with functions for imaging and modelling (pre-calibrated e.g. with AIPS) VLBI observations. These scripts are designed for automatic imaging and modeling of hundreds or thoustand 'typical' sources. The script was tested on the VIPS survey (https://arxiv.org/abs/1701.04037), nevertheless more simple examples are presented here.

Dependencies
============

The required dependiences to run the script:

- Python_ version 3.6+
- Numpy_ >= 1.11.3
- Matplotlib_ >= 2.0
- AstroPy_ >= 1.3
- difmap_ >= 2.4

The script was tested on Ubuntu 16.04.2 LTS release.

Development
===========


Authors
=======

Package Authos
--------------
* Kristóf Rozgonyi <rstofi@gmail.com> https://github.com/rstofi
* Frey Sándor <frey.sandor@csfk.mta.hu>

.. _Python: http://www.python.org
.. _Numpy: http://www.numpy.org
.. _Matplotlib: http://matplotlib.org
.. _AstroPy: http://www.astropy.org/
.. _difmap: http://ftp.astro.caltech.edu/pub/difmap/difmap.html
