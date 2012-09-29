# Scan probe files for:
# 
#  - display_name line
#  - <description> ... </description>

import os
import sys
import re

crlf    = "\r\n"
cr = "\r"
lf = "\n"
pTag = '<p class="proberef">'
closepTag = '</p>'
ulTag = '<li class="proberef">'
closeulTag = '</li>'

def outputdisplayname(path, infile):
	f = open(path+infile, 'r')
	#print "File is: " + infile
	while True:
		aLine = f.readline()
		if aLine == "":
			break
		bLine = aLine.lower()
		dispPat = re.compile("display_name.*?=")
		if dispPat.search(bLine) is not None:
			aLine = aLine.replace(crlf, "")      # remove crlf
			aLine = aLine.replace(cr, "")         # remove cr
			aLine = aLine.replace(lf, "")         # remove lf
			print infile + ": " + aLine
			f.close()
			return

# Emit good HTML code for this line
# To do:
# Uxxx
# * in first column could be <li>
# ignore comment anywhere (.*--) 

def htmlize(aLine):
	
	if aLine == "":							# empty line - ignore
		return None
	if aLine.find("--") == 0:				# comment at the start of line - ignore
		return None
	bLine = aLine.replace("\\", "#")		# convert '\' to '#' for easier parsing
 	bPat = re.compile("#[GB]+#(.*?)#[P][0-9]?#", re.I)
 	iPat = re.compile("#[ib]+#(.*?)#[P][0-9]?#", re.I)
# 	uPat = re.compile(r'^(.*):.*display_name["]?.*"(.*)"')

	cLine = re.sub(bPat, r"<b>\1</b>", bLine)
	cLine = re.sub(iPat, r"<i>\1</i>", cLine)
	if cLine[0] == "*" or cLine[0] == "-":	# bullet-ish character at front of line
		cLine = cLine[1:]
		cLine = ulTag + cLine + closeulTag
	return cLine + closepTag + lf + pTag	
	
def outputdescription(path, infile):
	f = open(path+infile, 'r')
	printing = False
	while True:
		aLine = f.readline()
		if aLine == "":
			break
		#print "Next line: '" + aLine + "'"
		aLine = aLine.replace(crlf, "")      # remove crlf
		aLine = aLine.replace(cr, "")         # remove cr
		aLine = aLine.replace(lf, "")         # remove lf
		bLine = aLine.lower()
		if bLine.find("<description>") != -1:
			aLine = pTag						# issue opening <p> tag
			printing = True						# start handling subsequent lines
		if bLine.find("</description>") != -1:	# Done! issue closing </p> tag
			print closepTag
			f.close()
			return
		if printing:
			bLine = htmlize(aLine)
			if bLine is not None:
				print bLine
		
	
path = '/Users/richb/Desktop/Newstuff/BuiltinProbes/'
listing = os.listdir(path)
for infile in listing:
    outputdisplayname(path, infile)
    outputdescription(path, infile)
    
