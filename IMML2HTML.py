# IMML2HTML.py
# Scan a file of IMML (InterMapper Markup Language) and output corresponding HTML
# Each line of the IMML is treated separately: there is no cross-line markup


import os
import sys
import re

crlf        = "\r\n"
cr          = "\r"
lf          = "\n"
pTag        = '<p class="proberef">'
closepTag   = '</p>'
liTag       = '<li class="proberef">'
closeliTag  = '</li>'

def CleanLineEndings(aLine):

    """
    Return the line, minus any trailing CR and LF
    """
    str = aLine.replace(cr, "")       # remove cr
    str = str.replace(lf, "")         # remove lf
    return str
    
def CleanMarkup(markup, urlString, tag):

    """
    The 'markup' string has the IMML tags
    Remove the named tags (usually m & g), as well as +, -, 0-9
    """
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
    
'''
ProcessPropMono - scan the line, looking for "g" and "m" markup
Emit the proper <code> and </code> tags, 
and remove the "g" and "m" markup from the returned line
'''
def ProcessPropMono(bLine):
    cLine = ""
    inMarkup = False
    inMono = False
    markup = ""                         # contains the markup characters up to a "=" (in URL)
    urlStr = ""                         # if present, contains "=" and the URL
    for c in bLine:						# character by character scan of the line
        if c == "\xb2" or c == "\xb3":	# fix up <= or >= markup from ancient probes
            c = "`"
        if c == "`":                    # start/end markup section
            if inMarkup:                # if we're already within markup
                inMarkup = False        # this is the end
                # Time to output the markup
                markup = markup.lower() # make lower case
                #print "Markup, looking for m: '" + s + "'<br />"
                if markup.find("m") != -1:    # found a "m" that's not in a URL
                    inMono = True
                    markup = CleanMarkup(markup, urlStr, "m")
                    cLine += markup + "<code>"
                elif markup.find("g") != -1:  # Found a "g" not in a URL
                    markup = CleanMarkup(markup, urlStr, "g")
                    if inMono:                # if we're in mono run, terminate it
                        cLine += "</code>"
                        inMono = False        # and remember that we're not
                    cLine += markup
                else:                    # regular markup
                    cLine += "`" + markup + urlStr + "`"
                c = markup = urlStr = "" # and clear accumulated markup 
                #print "The Line: '" + cLine + "'"
            else:
                inMarkup = True           # we're starting the markup
                markup= ""                # clear accumulator
                urlStr = ""
        elif len(urlStr) != 0:            # we're accumulating the URL string...            
            urlStr += c
        elif inMarkup:                    # Not a "`" but we're in markup
            if c == "=":                  # found a URL within the markup; no more "m" or "g" matter
                urlStr = "="              # starting the URL
                c = ""                    # consume the "=" - don't add to markup
                #print "Markup at start of URL: '" + markup + "' " + str(urlPos) + "<br />"
            markup += c                   # add to markup
        else:
            cLine += c                    # append the character to the output string
        #print "[" + markup + "]" + cLine + "<br />"
    if markup != "":
        cLine += "`" + markup             # append any accumulated markup
    if inMono:
        cLine += "</code>"                # 
    # print "End result: [" + markup + "]" + cLine + "<br />"
    return cLine
    
def IMMLtoHTML(aLine):
    
    """
	Emit reasonably attractive HTML code for this line
	A charactistic of IMML is that it tends to have one line to a paragraph
	Thus this function returns a line of <p ...> <the line> </p> lf
	
	IMML markup uses backslashes to delimit the IMML tags
	 (and also Mac <= and >= characters in ancient probes)
	Replace all "\" with "`" for ease of RE processing
	Put back all backslashes when complete
	
	Remove Proportional/Monospace markings from IMML within this line
	Assume we're in proportional ("G"). If \...m...\ encountered,
	   switch to monospace and follow by with '<code>'
	when we encounter closing \...g...\, precede with </code> and continue on
	when this is done, remove "g" & "m" from markup tags
	
	THIS CODE IS NOT VERY ROBUST! It works for all built-in probes, and
	  many sensible cases, but stressing IMML will generate inaccurate 
	  HTML representations

    """
    aLine = CleanLineEndings(aLine)		# remove line endings
    if aLine == "":                    	# ignore (strip out) empty line 
        return None
    if aLine.find("--") == 0:           # ignore comment at the start of line
        return None

    bLine = aLine.replace("\\", "`")    # convert '\' to '`' for parsing

    # Set up constant regular expressions
    bPat =  re.compile("`[-+b0-9]+?`(.*?)`[-+P0-9]+?`", re.I)        	# bold text
    iPat =  re.compile("`[-+i0-9]+?`(.*?)`[-+P0-9]+?`", re.I)        	# italic text
    ibPat = re.compile("`[-+ib0-9]+?`(.*?)`[-+P0-9]+?`", re.I)        	# italic & bold
    uPat =  re.compile("`[-+u0-9ib]+?`(.*?)`[-+P0-9]+?`", re.I)        	# just underlined text
    uhPat = re.compile("`[-+u0-9ib]+?`(http)(.*?)`[-+P0-9]+?`", re.I) 	# URL between markup
    uePat = re.compile("`[-+u0-9ib]+?=(.*?)`(.*?)`[-+P0-9]+?`", re.I) 	# URL within markup
    pPat =  re.compile("`[-+p0-9]+?`(.*?)`[-+P0-9]+?`", re.I)        	# \p\ ... \p\

    cLine = ProcessPropMono(bLine)									# handle prop. and monospace
    cLine = re.sub(iPat,  r"<i>\1</i>", cLine)                 		# italics
    cLine = re.sub(bPat,  r"<b>\1</b>", cLine)                 		# bolds
    cLine = re.sub(ibPat, r"<b><i>\1</i></b>", cLine)         		# bold italics
    cLine = re.sub(uePat, r'<a href="\1">\2</a>', cLine)    		# u=... (has URL within markup)
    cLine = re.sub(uhPat, r'<a href="\1\2">\1\2</a>', cLine)    	# u with URL (markup brackets URL)
    cLine = re.sub(uPat,  r'<u>\1</u>', cLine)                		# u... (underlined text)
    cLine = re.sub(pPat,  r'\1', cLine)                        		# \p\ ... \p\ is a no-op

#     print "'%s'" % aLine
#     print "'%s'" % cLine
    if cLine[0] == "*" or cLine[0] == "-":            	# bullet-ish character at front of line
        cLine = cLine[1:]
        cLine = liTag + cLine + closeliTag            	# wrap in <li> ... </li> tags
    cLine = cLine.replace("`", "\\")                	# finally put back bare '\'s
    cLine = pTag + cLine + closepTag
    return cLine

def main(argv=None):
    f = sys.stdin
    while True:
        line = f.readline()
        if line == "":
            break
        bline = IMMLtoHTML(line)
        if bline:
            print bline

if __name__ == "__main__":
    sys.exit(main())
