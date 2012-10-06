#!/bin/sh

# This is a set of commands to grep through all the InterMapper Probe files and:
# isolate all display_name and <description> ... </description> lines
# regularize them with a Python script
# Sort them into category order
# Output an HTML-formatted page that shows all the files

# USAGE
#   
#    sh ./updateprobe.sh [ defaults to reading built-in probes from local directory ]
#
# OUTPUTS
# 
# probedescr.txt - a file containing all the display_name and <definition> ... </definition> lines
# categories.txt - a file with the category names at the beginning of the line

python ScanForProbeFiles.py "$1" > probedescr.txt 
# python PrefixWithCategory.py < probedescr.txt > categories.txt
sort -t"|" -k1f,1 -k2,2 -k3n,3 < probedescr.txt \
  |	sed -e 's/^||1|/ /' \
  |	sed -e 's/^\(.*\)\|.*|1\|\(.*\)/<h2>\1<\/h2> /' \
  |	sed -e 's/^.*\|.*\|[0-9]*\|/	/' > ProvisionalProbeReference.html

