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
from os.path import join, getsize
import sys
import re
import datetime
import time
from IMML2HTML import IMMLtoHTML

crlf        = "\r\n"
cr          = "\r"
lf          = "\n"
pTag        = '<p class="content">'
closepTag   = '</p>'
liTag       = '<li class="content">'
closeliTag  = '</li>'

def usableFile(fname):
    '''
    check that the file name doesn't contain any useless path elements
    - anything path element staring with "." including: 
    	.hg
    	.hgignore
    	.git
    	.gitignore
    	.DS_Store
    	.index
    - CVS as the sole path element
    - xxxx.zip as a suffix
    - "MIB_Viewers" and "MIB Viewers" - they never contain anything interesting
    Returns true if none of these patterns match
    '''
    if fname.find(os.sep + ".") != -1:
        return False
    if fname.find(os.sep + "CVS" + os.sep) != -1:
    	return False
    if fname.find(os.sep + "MIB Viewers" + os.sep) != -1:
    	return False
    if fname.find(os.sep + "MIB_Viewers" + os.sep) != -1:
    	return False
    if fname.find(".zip") == (len(fname) - 4):
#        print "File: '%s'" % fname
#    	print "***File: '%s', Len: %d, Match: %d" % (fname, len(fname), fname.find(".zip"))
    	return False
    return True

def CleanLineEndings(aLine):

    """
    Return the line, minus any trailing CR and LF
    """
    str = aLine.replace(cr, "")       # remove cr
    str = str.replace(lf, "")         # remove lf
    return str
    
def GetProbeMetaInfo(probepath, infile):

    """
    Get the meta-info about the probe:
    Input:	
    - probepath is the directory that encloses all the probes
    - infile is the specific file to check
    
    Return: it as (display_name, filename, version)
    - display_name
    - filename including enclosing folder(s) if not at top level of probes folder
    - version

    """
    f = open(infile, 'r')
    #dispPat = re.compile("display_name")
    dispPat = re.compile(r'display_name.["]?.*"(.+)"', re.I)        
    namePat = re.compile(r'human_name.["]?.*"(.+)"', re.I)  # look for "human_name"      
    versPat = re.compile(r"version[\"\']?.*?=.*[\"\']?([0-9]+\.[0-9]+)", re.I)
    displayName = ""
    version = ""
    humanname = ""
    while displayName == "" or version == "":
        aLine = f.readline()
        if aLine == "":
            break
        aLine = CleanLineEndings(aLine)
        # bLine = aLine
        matches = dispPat.search(aLine)
        if matches:
            displayName = matches.group(1)
        matches = versPat.search(aLine)
        if matches:
            version = matches.group(1)
        matches = namePat.search(aLine)
        if matches:
            humanname = matches.group(1)
            #print "***Found HumanName: '%s'; human_name: '%s'" % (aLine, humanname)
#    else:
#        print "Fell off end of file****"
        
    f.close()
    
    if displayName == "" and humanname != "":	# some probes don't have "display_name"
        # print "***Line: '%s'; human_name: '%s'" % (bLine, humanname)
        displayName = "Uncategorized/" + humanname  # just use the human name
    if displayName.find("/") == -1:
        displayName = "Uncategorized/" + displayName  # No category? Add "Uncategorized/"

    # clean up the path
    enclosingpath = infile[len(probepath):]
    # print "Enclosing path: '%s'" % enclosingpath
    return (displayName, enclosingpath, version)


def GetProbeDescription(infile):

    """
    Scan through the file line by line
    Find all the lines between <description> and </description>
    Change each line from IMML to HTML
    Return a list of the HTML-ized lines without line endings
    """
    f = open(infile, 'r')
    # print "Opening: '" + infile + "'<br />"

    printing = False
    notDone = True                                # set to false when we hit closing </description>
    result = []
    while notDone:
        aLine = f.readline()
        #print infile + ":" + aLine + "<br />"
        if aLine == "":
            break
        aLine = CleanLineEndings(aLine)
        bLine = aLine.lower()
        if bLine.find("<description>") != -1:
            aLine = ""                            # issue opening <p> tag
            printing = True                        # start handling subsequent lines
        if bLine.find("</description>") != -1:    # Done! issue closing </p> tag
            aLine = ""
            f.close()
            notDone = False
        if printing:
            bLine = IMMLtoHTML(aLine)
            # resultstr += bLine
            if bLine is not None:
                result.append(bLine)
    return result

def ProcessProbeFile(probepath, infile):

    """
    Process each probe file:
       scan to find the file's display_name (to get its category)
       pull out the <description> section
       Append the filename and version numbers
    """
    (category, filename, version) = GetProbeMetaInfo(probepath, infile)
    if category == "" or version == "":              # couldn't find category or version
        # print "*** Bad News - File: %s; Category '%s'; Version '%s'" % (filename, category, version)
        return None
    definitions = GetProbeDescription(infile)        # couldn't find <definitions>
    if len(definitions) == 0:
        return None
    
    # Output lines have the form: 
    #   category|filename|1|version
    #   category|filename|2|<blockquote>
    #   category|filename|3| HTML-ized line1
    #   category|filename|4| HTML-ized line2
    #	...
    #   category|filename|n-1| HTML-ized line n-2
    #   category|filename|n| </blockquote>

    print "%s|%s|%d|%s" % (category, filename, 1, version)
    print "%s|%s|%d|%s" % (category, filename, 2, "<blockquote>")
    for i in range(len(definitions)):
        print "%s|%s|%d|%s" % (category, filename, i+2, definitions[i])
    print "%s|%s|%d|%s" % (category, filename, i+3, "</blockquote>"+pTag)    
    print "%s|%s|%d|%s" % (category, filename, i+4, "<i>Filename: "+filename+"</i><br />")    
    print "%s|%s|%d|%s" % (category, filename, i+5, "<i>Version: "+version+"</i><br />")    
    print "%s|%s|%d|%s" % (category, filename, i+6, closepTag)    
    
#     print filename + ": " + category
#     print "<blockquote>" + definitions + "</blockquote>" + lf + pTag
#     print "<i>Filename: " + filename + "</i><br />"
#     print "<i>Version: " + version + "</i>"
#     print closepTag


# Main Routine
# For each file from designated directory
#     Scan them for interesting meta info
#     (Category, file name, version, date last modified)
#     Retrieve the <definitions> section
#     Output the information in the proper format
def main(argv=None):

    # path = './'
    # infile = 'com.dartware.email.imap.txt'
    # ProcessProbeFile(path, infile)

    args = sys.argv[1:]                      # retrieve the arguments
    if len(args) == 0:                       # handle missing argument
        arg = ""
    else:
        arg = args[0]
    
    probepath = arg
    if probepath == "":						# build path to local copy of probes
        wd = os.getcwd()
        probepath = join(wd, 'BuiltinProbes')
    if probepath[-1] != os.sep:				# make sure the path ends in separator
        probepath += os.sep
    # print probepath
    # print "Hi Rich"
    
    listing = []
    # walk the root directry, build a list of all the non-directory files
    for root, dirs, files in os.walk(probepath):
        for name in files:
            fname = join(root, name)
            if (usableFile(fname)):
                listing.append(fname)    




    # Print heading info with date
    today = str(datetime.date.today())
    print "||1|<link rel='stylesheet' type='text/css' href='http://www.intermapper.com/library/styles/client.css' />"
    print "||2|<h1>InterMapper Probe Documentation</h1>"
    print "||3|%s<i>Base Folder: %s</br />" % (pTag, probepath)
    print "||4|Updated: " + time.strftime('%l:%M%p %Z on %b %d, %Y') + "</i>" + closepTag
    
#     for dir, file in listing:
#         print "File: '%s' in '%s'" % (file, dir)
        
    # at this point, listing contains a list of filenames to process
    for infile in listing:
        ProcessProbeFile(probepath, infile)
            
if __name__ == "__main__":
    sys.exit(main())
