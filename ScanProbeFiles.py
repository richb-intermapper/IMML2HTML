# Scan probe files for:
# 
#  - display_name line
#  - <description> ... </description>

# To do:
# handle Uxxx in IMML
# ignore comment anywhere (.*--) 
# Handle a folder hierarchy of probes
# segregate file name, version, date info, etc. below info for each probe

import os
import sys
import re
import datetime
import time

crlf    	= "\r\n"
cr 			= "\r"
lf 			= "\n"
pTag 		= '<p class="proberef">'
closepTag 	= '</p>'
liTag		= '<li class="proberef">'
closeliTag 	= '</li>'

def CleanLineEndings(aLine):
	aLine = aLine.replace(crlf, "")      # remove crlf
	aLine = aLine.replace(cr, "")         # remove cr
	aLine = aLine.replace(lf, "")         # remove lf
	return aLine
	
# Clean up markup string
# remove the tag (M or G), and +, -, 0-9
def CleanMarkup(markup, urlString, tag):
	result = markup
	chars = set("0123456789+-" + tag)
	i = 0
	while i < len(result):
		if result[i] in chars:
			result = result[:i] + result[(i+1):]
		else:
			i += 1
	result = result + urlString
	if result != "":
		result = "`" + result + "`"
	# print "Cleaned markup: '" + markup + "|" + result + "' <br />"
	return result
	
# Get the meta-info about the probe:
# - display_name
# - filename
# - version
# return it as (display_name, filename, version)
def GetProbeMetaInfo(path, infile):
	f = open(path+infile, 'r')

#	dispPat = re.compile("display_name.*?=")
	dispPat = re.compile("display_name")
	versPat = re.compile(r"version.*?=.*[\"\']?([0-9.]+)")
	displayName = ""
	version = ""
	while displayName == "" or version == "":
		aLine = f.readline()
		if aLine == "":
			break
		bLine = aLine.lower()
		if dispPat.search(bLine) is not None:
			displayName = CleanLineEndings(aLine)
#			print "Found Display Name*****:" + infile + ": " + aLine
		if versPat.search(bLine) is not None:
#			print "Found Version*****"
			version = "123.45"
#	else:
#		print "Fell off end of file****"
		
	f.close()
	return (displayName, infile, version)

# Emit attractive HTML code for this line
# Replace all "\" with "`" for ease of RE processing
# Put back all backslashes when complete

def IMMLtoHTML(aLine):
	
	if aLine == "":							# empty line - ignore
		return None
	if aLine.find("--") == 0:				# comment at the start of line - ignore
		return None

# Remove Proportional/Monospace markings from IMML within this line
# Assume we're in proportional ("G"). If \...m...\ encountered, 
#	switch to monospace and follow by with '<code>'
# when we encounter closing \...g...\, precede with </code> and continue on

	bLine = aLine.replace("\\", "`")	# convert '\' to '`' for parsing
	cLine = ""
	inMarkup = False
	inMono = False
	markup = ""							# contains the markup characters up to a "=" (in URL)
	urlStr = ""							# if present, contains "=" and the URL
	for c in bLine:
		if c == "`":					# start/end markup section
			if inMarkup:				# if we're already within markup
				inMarkup = False		# this is the end
				# Time to output the markup
				markup = markup.lower() # make lower case
				#print "Markup, looking for m: '" + s + "'<br />"
				if markup.find("m") != -1:	# found a "m" that's not in a URL
					inMono = True
					markup = CleanMarkup(markup, urlStr, "m")
					cLine += markup + "<code>"
				elif markup.find("g") != -1: # Found a "g" not in a URL
					markup = CleanMarkup(markup, urlStr, "g")
					if inMono:			# if we're in mono run, terminate it
						cLine += "</code>"
						inMono = False	# and remember that we're not
					cLine += markup
				else:					# regular markup
					cLine += "`" + markup + urlStr + "`"
				c = markup = urlStr = "" # and clear accumulated markup 
				#print "The Line: '" + cLine + "'"
			else:
				inMarkup = True			# we're starting the markup
				markup= ""				# clear accumulator
				urlStr = ""
		elif len(urlStr) != 0:			# we're accumulating the URL string...			
			urlStr += c
		elif inMarkup:					# Not a "`" but we're in markup
			if c == "=":				# found a URL within the markup; no more "m" or "g" matter
				urlStr = "="			# starting the URL
				c = ""					# consume the "=" - don't add to markup
				#print "Markup at start of URL: '" + markup + "' " + str(urlPos) + "<br />"
			markup += c					# add to markup
		else:
			cLine += c					# append the character to the output string
		#print "[" + markup + "]" + cLine + "<br />"
	if markup != "":
		cLine += "`" + markup			# append any accumulated markup
	if inMono:
		cLine += "</code>"				# 
	# print "End result: [" + markup + "]" + cLine + "<br />"

# Set up constant regular expressions
 	bPat =  re.compile("`[-+b0-9]+?`(.*?)`[-+P0-9]+?`", re.I)		# bold text
 	iPat =  re.compile("`[-+i0-9]+?`(.*?)`[-+P0-9]+?`", re.I)		# italic text
 	ibPat = re.compile("`[-+ib0-9]+?`(.*?)`[-+P0-9]+?`", re.I)		# italic & bold
 	uPat =  re.compile("`[-+u0-9ib]+?`(.*?)`[-+P0-9]+?`", re.I)		# just underlined text
 	uhPat = re.compile("`[-+u0-9ib]+?`(http)(.*?)`[-+P0-9]+?`", re.I) # URL between markup
 	uePat = re.compile("`[-+u0-9ib]+?=(.*?)`(.*?)`[-+P0-9]+?`", re.I) # URL within markup
 	pPat =  re.compile("`[-+p0-9]+?`(.*?)`[-+P0-9]+?`", re.I)		# \p\ ... \p\

#	cLine = re.sub(mPat,  r"<code>\1</code>", cLine) 		# monospace
	cLine = re.sub(iPat,  r"<i>\1</i>", cLine) 				# italics
	cLine = re.sub(bPat,  r"<b>\1</b>", cLine) 				# bolds
	cLine = re.sub(ibPat, r"<b><i>\1</i></b>", cLine) 		# bold italics
	cLine = re.sub(uePat, r'<a href="\1">\2</a>', cLine)	# u=... (has URL within markup)
	cLine = re.sub(uhPat, r'<a href="\1\2">\1\2</a>', cLine)	# u with URL (markup brackets URL)
	cLine = re.sub(uPat,  r'<u>\1</u>', cLine)				# u... (underlined text)
	cLine = re.sub(pPat,  r'\1', cLine)						# \p\ ... \p\ is a no-op

	if cLine[0] == "*" or cLine[0] == "-":			# bullet-ish character at front of line
		cLine = cLine[1:]
		cLine = liTag + cLine + closeliTag			# wrap in <li> ... </li> tags
	cLine = cLine.replace("`", "\\")				# finally put back bare '\'s
	return cLine + closepTag + lf + pTag	

def GetProbeDescription(path, infile):
	f = open(path+infile, 'r')
	printing = False
	notDone = True								# set to false when we hit closing </description>
	resultstr = ""
	while notDone:
		aLine = f.readline()
		aLine = CleanLineEndings(aLine)
		if aLine == "":
			break
		#print "Next line: '" + aLine + "'"
		bLine = aLine.lower()
		if bLine.find("<description>") != -1:
			aLine = pTag						# issue opening <p> tag
			printing = True						# start handling subsequent lines
		if bLine.find("</description>") != -1:	# Done! issue closing </p> tag
			aLine = closepTag
			f.close()
			notDone = False
		if printing:
			bLine = IMMLtoHTML(aLine)
			if bLine is not None:
				resultstr += bLine
	return resultstr

def ProcessProbeFile(path, ifile):
	(category, filename, version) = GetProbeMetaInfo(path, infile)
	definitions = GetProbeDescription(path, infile)
	
# output header line
	print filename + ": " + category
	print "<blockquote>" + definitions + "</blockquote>" + pTag
	print "<i>Filename: " + filename + "</i><br />"
	print "<i>Version: " + version + "</i>"
	print closepTag

# Main Routine
# For each file from designated directory
# 	Scan them for interesting meta info
#     (Category, file name, version, date last modified)
# 	Retrieve the <definitions> section
# 	Output the information in the proper format

# Print heading info with date
# today = str(datetime.date.today())
# print pTag
# print "<h1>InterMapper Builtin Probe Reference</h1>"
# print "<i>Updated: " + today + time.strftime('%l:%M%p %Z on %b %d, %Y') + "</i>"
# print closepTag

# path = './'
# infile = 'testtags.txt'
# ProcessProbeFile(path, infile)

path = '/Users/richb/Desktop/Newstuff/BuiltinProbes/'
listing = os.listdir(path)

for infile in listing:
	ProcessProbeFile(path, infile)
