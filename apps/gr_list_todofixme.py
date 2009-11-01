#!/usr/bin/env python

#a page for each category with all the files
#a page for each file with all the categories

from Cheetah import Template as _Template
def Template(_tmpl_str, **kwargs): return str(_Template.Template(_tmpl_str, kwargs))

import re
import os
import sys
import glob
import todofixme

parser = todofixme.parser()
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)todo\s.*').match, category='TODO')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)fixme\s.*').match, category='FIXME')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)magic\s.*').match, category='Magic')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)kludge\s.*').match, category='Kludges')

TMPL="""
<html>
	<head>
		<title>Gnuradio TODOs, FIXMEs, etc...</title>
	</head>
	<body>
		<h1>Gnuradio TODOs, FIXMEs, etc...</h1>
		####### build toc #######
		<ul>
		#for $chunk in $chunks
			<li><a href="#$chunk.get_file()">$chunk.get_file()</a></li>
		#end for
		</ul>
		####### file list #######
		###for $chunk in $chunks
		<a name="$chunk.get_file()" />
		##<h2>$chunk.get_file()</h2>
			###for $i, $chunk in enumerate($result.get_chunks())
				##<h3>$chunk.get_category() $(i+1)</h3>
				##<p>
				##	#for $lineno, $line in enumerate($chunk.get_lines())
				##		#if $chunk.get_lineno()-3 < $lineno < $chunk.get_lineno()+6
				##	$lineno        $line<br />
				##		#end if
				##	#end for
				##</p>
			###end for
		###end for
	</body>
</html>
"""

def matcher(file_name):
	blacklist = ('gnuradio_swig_py_general.cc', 'Makefile.in')
	if file_name in blacklist: return False
	return re.compile('^(\w*\.(m4|am|in|ac|py|c|cc|h|t))$').match(file_name)

if __name__ == '__main__':
	results = list()
	files = todofixme.get_matching_files(sys.argv[1], matcher)
	result = parser(files, path=sys.argv[1])
	open('out.html', 'w').write(Template(TMPL, chunks=result.get_chunks()))
