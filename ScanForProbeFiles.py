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
pTag        = '<p class="proberef">'
closepTag   = '</p>'
liTag       = '<li class="proberef">'
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
    Returns true if none of these patterns match
    '''
    if fname.find(os.sep + ".") != -1:
        return False
    if fname.find(os.sep + "CVS" + os.sep) != -1:
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
    dispPat = re.compile("display_name.*?=")        
    namePat = re.compile("human_name.*?=")  # look for "human_name"      
    versPat = re.compile(r"version[\"\']?.*?=.*[\"\']?([0-9]+\.[0-9]+)")
    displayName = ""
    version = ""
    humanname = ""
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
        matches = namePat.search(bLine)
        if matches:
            humanname = matches.group(1)
#    else:
#        print "Fell off end of file****"
        
    f.close()
    
    if displayName == "":							# some probes don't have "display_name"
        displayName = "Uncategorized/" + humanname  # just use the human name
        
    # clean up the path
    enclosingpath = infile[len(probepath):]
    # print "Enclosing path: '%s'" % enclosingpath
    return (displayName, enclosingpath, version)


def GetProbeDescription(infile):

    """
    Scan through the file line by line
    Find all the lines between <description> and </description>
    Change each line from IMML to HTML
    """
    f = open(infile, 'r')
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
                resultstr += bLine + lf
    return resultstr

def ProcessProbeFile(probepath, infile):

    """
    Process each probe file:
       scan to find the file's display_name (to get its category)
       pull out the <description> section
       Append the filename and version numbers
    """
    (category, filename, version) = GetProbeMetaInfo(probepath, infile)
    if category == "" or version == "":              # couldn't find category or version
        print "*** Bad News - File: %s; Category '%s'; Version '%s'" % (filename, category, version)
        return None
    definitions = GetProbeDescription(infile)        # couldn't find <definitions>
    if definitions == "":
        return None
    
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
def main(argv=None):

    # Print heading info with date
    today = str(datetime.date.today())
    print ":|1|"
    print ":|2|<description>"
    print ":|3|<h1>InterMapper Builtin Probe Documentation</h1>"
    print ":|4|<i>Updated: " + time.strftime('%l:%M%p %Z on %b %d, %Y') + "</i>"
    
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
    # print probepath
    # print "Hi Rich"
    
    listing = []
    # walk the root directry, build a list of all the non-directory files
    for root, dirs, files in os.walk(probepath):
        for name in files:
            fname = join(root, name)
            if (usableFile(fname)):
                listing.append(fname)    

#     for dir, file in listing:
#         print "File: '%s' in '%s'" % (file, dir)
        
    # at this point, listing contains a list of filenames to process
    for infile in listing:
        ProcessProbeFile(probepath, infile)
            
if __name__ == "__main__":
    sys.exit(main())
