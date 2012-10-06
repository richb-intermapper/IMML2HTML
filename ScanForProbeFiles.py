# Scan a directory of files for InterMapper probe files
# 
# Detect the probe file by the presence of <description> ... </description>
# 
# Extract the definition lines and the probe meta info which includes:
# - Probe Category (Servers Standard/HTTP & HTTPS/HTTP)
# - Probe version
# - Full probe path info
# 

import os
import sys
import re
import datetime
import time

crlf        = "\r\n"
cr          = "\r"
lf          = "\n"

def CleanLineEndings(aLine):

    """
    Return the line, minus any trailing CR and LF
    """
    str = aLine.replace(cr, "")       # remove cr
    str = str.replace(lf, "")         # remove lf
    return str
    
def GetProbeMetaInfo(path, infile):

    """
	Get the meta-info about the probe:
	- display_name
	- filename
	- version
	return it as (display_name, filename, version)

    """
    f = open(path+infile, 'r')
    #dispPat = re.compile("display_name")
    dispPat = re.compile("display_name.*?=")		
    versPat = re.compile(r"version[\"\']?.*?=.*[\"\']?([0-9]+\.[0-9]+)")
    displayName = ""
    version = ""
    while displayName == "" or version == "":
        aLine = f.readline()
        if aLine == "":
            break
        bLine = aLine.lower()
        if dispPat.search(bLine) is not None:
            displayName = CleanLineEndings(aLine)
        matches = versPat.search(bLine)
        if matches:
            version = matches.group(1)
#    else:
#        print "Fell off end of file****"
        
    f.close()
    return (displayName, infile, version)

def GetProbeDescription(path, infile):

    """
    Scan through the file line by line
    Find all the lines between <description> and </description>
    Change each line from IMML to HTML
    """
    f = open(path+infile, 'r')
    # print "Opening: '" + infile + "'<br />"

    printing = False
    notDone = True                                # set to false when we hit closing </description>
    resultstr = ""
    while notDone:
        aLine = f.readline()
        #print infile + ":" + aLine + "<br />"
        if aLine == "":
            break
        aLine = CleanLineEndings(aLine)
        bLine = aLine.lower()
        if bLine.find("<description>") != -1:
            aLine = ""                        	# issue opening <p> tag
            printing = True                        # start handling subsequent lines
        if bLine.find("</description>") != -1:    # Done! issue closing </p> tag
            aLine = ""
            f.close()
            notDone = False
        if printing:
            bLine = IMMLtoHTML(aLine)
            # resultstr += bLine
            if bLine is not None:
                resultstr += bLine
    return resultstr

def ProcessProbeFile(path, ifile):

    """
    Process each probe file:
       scan to find the file's display_name (to get its category)
       pull out the <description> section
       Append the filename and version numbers
    """
    (category, filename, version) = GetProbeMetaInfo(path, infile)
    definitions = GetProbeDescription(path, infile)
    
    # output header line
    print filename + ": " + category
    print "<blockquote>" + definitions + "</blockquote>" + lf + pTag
    print "<i>Filename: " + filename + "</i><br />"
    print "<i>Version: " + version + "</i>"
    print closepTag


# Main Routine
# For each file from designated directory
#     Scan them for interesting meta info
#     (Category, file name, version, date last modified)
#     Retrieve the <definitions> section
#     Output the information in the proper format

# Print heading info with date
today = str(datetime.date.today())
print ":|1|"
print ":|2|<description>"
print ":|3|<h1>InterMapper Builtin Probe Documentation</h1>"
print ":|4|<i>Updated: " + time.strftime('%l:%M%p %Z on %b %d, %Y') + "</i>"

# path = './'
# infile = 'com.dartware.email.imap.txt'
# ProcessProbeFile(path, infile)

path = './BuiltinProbes/'
listing = os.listdir(path)

for infile in listing:
    if infile[0] != ".":
        ProcessProbeFile(path, infile)
