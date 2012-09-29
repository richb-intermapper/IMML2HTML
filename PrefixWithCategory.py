# PrefixWithCategory.py
# Uses the output of this grep to isolate the probe's display_name and <description>
# pcregrep -M -e '(?s)(<description>\s*?.*?<\/description>)' -e display_name * > ~/Desktop/Junk/probedescr.txt
#
# Format of the Input:
#
# com.dartware.wrls.tranzeo.gen6ap.txt:	"display_name"		=	"Wireless/Tranzeo/Sixth Generation AP"
# com.dartware.wrls.tranzeo.gen6ap.txt:<description>
# 
# \GB\Tranzeo Sixth Generation AP\P\
# ...
# </description>
# 
# Format of the Output:
#
# Wireless/Tranzeo/Sixth Generation AP: com.dartware.wrls.tranzeo.gen6ap.txt
# Wireless/Tranzeo/Sixth Generation AP: <description>
# Wireless/Tranzeo/Sixth Generation AP: 
# Wireless/Tranzeo/Sixth Generation AP: \GB\Tranzeo Sixth Generation AP\P\
# Wireless/Tranzeo/Sixth Generation AP: ...
# Wireless/Tranzeo/Sixth Generation AP: </description>

import os
import sys
import re

filename = ""
category = ""
crlf    = "\r\n"
cr = "\r"
lf = "\n"
catPat = re.compile(r'^(.*):.*display_name["]?.*"(.*)"')
descriptionPat = re.compile(r'<description>')

# Process the file
f = sys.stdin							# open stdin
i = 1
while True:
	aLine = f.readline()
	if aLine == "":
		break
	aLine = aLine.replace(crlf, "")      # remove crlf
	aLine = aLine.replace(cr, "")         # remove cr
	aLine = aLine.replace(lf, "")         # remove lf
	catMatch = catPat.search(aLine)
	descrMatch = descriptionPat.search(aLine)

	if catMatch is not None:
		(filename, category) = catMatch.groups()
		print category + ":|1|" + filename
		print category + ":|2|<description>"
		i = 3
	elif descrMatch is not None:                    # found opening <description>
		# just ignore this line
		i = i
	else:
		print category + ":|" + str(i) + "|" + aLine
		i += 1

