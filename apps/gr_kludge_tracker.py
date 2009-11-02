#!/usr/bin/env python

import re
import os
import sys
import kludgetracker
from optparse import OptionParser

gr_ktp = kludgetracker.parser()
gr_ktp.register_matcher(re.compile('(?i).*(#|//|/\*|\s)todo\s.*').match, category='TODO')
gr_ktp.register_matcher(re.compile('(?i).*(#|//|/\*|\s)fixme\s.*').match, category='FIXME')
gr_ktp.register_matcher(re.compile('(?i).*(#|//|/\*|\s)magic\s.*').match, category='Magic')
gr_ktp.register_matcher(re.compile('(?i).*(#|//|/\*|\s)kludge\s.*').match, category='Kludge')

def file_matcher(file_name):
	blacklist = ('gnuradio_swig_py_general.cc', 'Makefile.in')
	if file_name in blacklist: return False
	return re.compile('^((\w*\.)*(m4|am|in|ac|py|c|cc|h|t|v|common))$').match(file_name)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("--src-dir", type="string", default=None)
	parser.add_option("--html-dir", type="string", default='html')
	parser.add_option("--desc", type="string", default='unknown version')
	(options, args) = parser.parse_args()

	results = list()
	files = kludgetracker.get_matching_files(options.src_dir, file_matcher)
	result = gr_ktp(files, path=os.path.dirname(options.src_dir))
	gen = kludgetracker.generator(result, title='Gnuradio - %s'%options.desc)
	gen.generate(options.html_dir)
