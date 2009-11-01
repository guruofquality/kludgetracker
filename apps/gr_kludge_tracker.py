#!/usr/bin/env python

import re
import sys
import kludgetracker

parser = kludgetracker.parser()
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)todo\s.*').match, category='TODO')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)fixme\s.*').match, category='FIXME')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)magic\s.*').match, category='Magic')
parser.register_matcher(re.compile('(?i).*(#|//|/\*|\s)kludge\s.*').match, category='Kludge')

def file_matcher(file_name):
	blacklist = ('gnuradio_swig_py_general.cc', 'Makefile.in')
	if file_name in blacklist: return False
	return re.compile('^((\w*\.)*(m4|am|in|ac|py|c|cc|h|t))$').match(file_name)

if __name__ == '__main__':
	results = list()
	files = kludgetracker.get_matching_files(sys.argv[1], file_matcher)
	result = parser(files, path=sys.argv[1])
	kludgetracker.generator(result, title='Gnuradio').generate('html')
