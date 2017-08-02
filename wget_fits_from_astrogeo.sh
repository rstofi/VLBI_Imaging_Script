#!/bin/bash
#
#This is a Linux shell script for download *.fits files from http://astrogeo.org
#
#Example usage for download all fits file of the source J001+914:
#>wget -nd -l 0 -r -A fits -e robots=off --no-parent http://astrogeo.org/images/J0001+1914/

wget -nd -l 0 -r -A fits -e robots=off --no-parent --accept "*.fits" http://astrogeo.org/images/source_name/

