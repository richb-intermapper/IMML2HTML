#!/bin/sh

# This is a set of commands to grep through all the InterMapper Probe files and:
# isolate all display_name and <description> ... </description> lines
# regularize them with a Python script
# Sort them into category order
# Output an HTML-formatted page that shows all the files

# USAGE
#   
#    sh ./updateprobe.sh [ defaults to reading probes from ~/Desktop/NewStuff/BuiltinProbes ]
#
# OUTPUTS
# 
# probedescr.txtl - a file containing all the display_name and <definition> ... </definition> lines
# categories.txt - a file with the category names at the beginning of the line

python ScanForProbeFiles.py > probedescr.txt
python PrefixWithCategory.py < probedescr.txt > categories.txt
sort -t"|" -k1,1 -k2n,2 < categories.txt \
  |	sed -e 's/^\(.*\):\|1\|\(.*\)/<h2>\1<\/h2> /' \
  |	sed -e 's/^.*:\|[0-9]*\|/	/' > ProvisionalProbeReference.html

# pcregrep -M -e '(?s)(<header>\s*?.*?<\/header>)' -e '(?s)(<description>\s*?.*?<\/description>)' * > ~/Documents/src/Probe->HTML/probesections.txt
# cd ~/Desktop/Junk/

# This is a set of commands to:
#	remove all "normal lines" with status 200, 206, 301, 302, 304, etc.
# 	remove any silvertech.net lines (why are they there?)
#	remove the comments at the beginning of the file (#....)
#	parse out the status of the line, put it in (###) at the front
#	clean up the line to remove time stamp up to the command (GET, HEAD, POST)
#	   retaining the HEAD & POST
#   fix up the go.php scripts that lose their "?"
#   fix up the other URLs that are missing the "?" in the " format=..."
#   fix up the atom & rss feed lines, as well.
#   convert all runs of spaces to a tab
#   tee the result to a file "alllines.txt" for future work
#   sort the file on the first column, keeping one copy of duplicated lines. 

# USAGE
#   sh ./filter404.sh inputfilename 
	
# grep -vi "intermapper.com 200" < $1 \
# 	| grep -vi "intermapper.com 206" \
# 	| grep -vi "intermapper.com 301" \
# 	| grep -vi "intermapper.com 302" \
# 	| grep -vi "intermapper.com 304" \
# 	| grep -vi "silvertech.net" \
# 	| grep -v "^#.*:" \
# 	| sed -e 's/\(.*www\.intermapper\.com\) \(...\)/(\2)\1/' \
# 	| sed -e 's/).*GET /)/' \
# 	| sed -e 's/).*HEAD /_HEAD)/' \
# 	| sed -e 's/).*POST /_POST)/' > other.txt
# 	
# cat other.txt \
# 	| sed -e 's/go\.php /go\.php\?/' \
# 	| sed -e 's/news-details\.aspx /news-details\.aspx\?/' \
# 	| sed -e 's/ format=/\?format=/' \
# 	| sed -e 's/type=atom /type=atom - /' \
# 	| sed -e 's/type=rss /type=rss - /' \
# 	| tr -s '[:blank:]' '\t' \
# 	| tee alllines.txt \
# 	| sort -u -k 1,1 > $1.output.txt
# 
# # print total number of lines in the alllines.txt file
# 
# echo "There were `wc -l < alllines.txt` lines with unusual status. "\
# | tee $1.html
# 
# echo "<br />\n" | cat >> $1.html
# 
# # print the most frequent 20 lines
# # process the alllines.txt file to chop off the first column then sort
# 
# sort alllines.txt \
# 	| cut -f1 \
# 	| tee firstcolumn.txt \
# 	| uniq -c \
# 	| sort -r \
# 	| head -20
# 
# # Create an HTML file of all the bad URLs for testing in the future
# # processes the file firstcolumn.txt to wrap in <a href="...">...</a>
# 
# sed -e 's@^\([^/]*\)\(.*\)$@<a href=\"http://intermapper.com\2\">\2<\/a>  \1<br \/>@' < firstcolumn.txt \
# 	| uniq -c \
# 	| sort -r >> $1.html
