#!/usr/bin/env python

import re
import os
import optparse
import commands
import kludgetracker

def pyflakes_matcher(file_name):
	if not file_name.endswith('.py'): return ()
	lines = commands.getoutput('pyflakes "%s"'%file_name).splitlines()
	results = list()
	for line in lines:
		try:
			lineno, message = re.match('^.*:(\d*):(.*)$', line).groups()
			#pyflakes messages that we intend to skip:
			if message.endswith('imported but unused'): continue
			if message.endswith('but never used'): continue
			if message.endswith('unable to detect undefined names'): continue
			results.append((int(lineno)-1, message))
		except: pass
	return results

def file_matcher(file_name):
	blacklist = ('gnuradio_swig_py_general.cc', 'Makefile.in')
	if file_name in blacklist: return False
	return re.compile('^((\w*\.)*(m4|am|in|ac|py|c|cc|i|h|t|v|common))$').match(file_name)

if __name__ == '__main__':
	#setup the option parser
	parser = optparse.OptionParser()
	parser.add_option("--src-dir", type="string", default=None)
	parser.add_option("--html-dir", type="string", default='html')
	parser.add_option("--desc", type="string", default='unknown version')
	(options, args) = parser.parse_args()

	#setup the kludge tracker parser
	ktp = kludgetracker.parser()
	ktp.register_line_matcher(re.compile('(?i).*(#|//|/\*|\s)todo\s.*').match,   category='TODO')
	ktp.register_line_matcher(re.compile('(?i).*(#|//|/\*|\s)fixme\s.*').match,  category='FIXME')
	ktp.register_line_matcher(re.compile('(?i).*(#|//|/\*|\s)magic\s.*').match,  category='Magic')
	ktp.register_line_matcher(re.compile('(?i).*(#|//|/\*|\s)kludge\s.*').match, category='Kludge')
	ktp.register_file_matcher(pyflakes_matcher,                                  category='PyFlakes')

	#parse and generate
	files = kludgetracker.get_matching_files(options.src_dir, file_matcher)
	result = ktp(files, path=os.path.dirname(os.path.abspath(options.src_dir)))
	gen = kludgetracker.generator(result, title='Gnuradio - %s'%options.desc)
	gen.generate(options.html_dir)
	print 'Done'
