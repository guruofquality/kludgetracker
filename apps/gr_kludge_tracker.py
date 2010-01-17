#!/usr/bin/env python

import re
import os
import optparse
import subprocess
import kludgetracker

def command(*args):
	return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]

def git_command(dir, *args):
	"""
	Call a git command and return the output.
	The directory must be changed before calling the command.
	And the directory must be restored before returning.
	"""
	cwd = os.getcwd()
	os.chdir(dir)
	output = command('git', *args)
	os.chdir(cwd)
	return output

def git_blame(file_name, lineno):
	"""
	Get the git blame information for a particular line in a file.
	Return a list of (key, value) tuples with blame information.
	"""
	try:
		lines = git_command(
			os.path.dirname(file_name),
			'blame', file_name, '--incremental',
			'-L', '%d,%d'%(lineno+1, lineno+1),
		).splitlines()
		items = dict([(line+' ').split(' ', 1) for line in lines])
		return (
			('Committer', items['committer']),
			('Commit ID', lines[0].split()[0]),
		)
	except Exception, e: return [('Error', str(e))]

def pyflakes_matcher(file_name, handler):
	"""
	A matcher function that calls pyflakes on a file.
	"""
	if not file_name.endswith('.py'): return ()
	for line in command('pyflakes', file_name).splitlines():
		try:
			lineno, message = re.match('^.*:(\d*):(.*)$', line).groups()
			#pyflakes messages that we intend to skip:
			if message.endswith('imported but unused'): continue
			if message.endswith('but never used'): continue
			if message.endswith('unable to detect undefined names'): continue
			lineno = int(lineno) - 1
			handler(lineno, ('PyFlakes', message), *git_blame(file_name, lineno))
		except: pass

def re_line_matcher(file_name, handler):
	"""
	A matcher function that calls various regular expressions.
	Each line of the file will be passed through the regexp.
	"""
	for lineno, line in enumerate(open(file_name, 'r').readlines()):
		for matcher, category in (
			(re.compile('(?i).*(#|//|/\*|\s)todo\s.*').match,   'TODO'),
			(re.compile('(?i).*(#|//|/\*|\s)fixme\s.*').match,  'FIXME'),
			(re.compile('(?i).*(#|//|/\*|\s)magic\s.*').match,  'Magic'),
			(re.compile('(?i).*(#|//|/\*|\s)kludge\s.*').match, 'Kludge'),
		):
			if not matcher(line): continue
			handler(lineno, ('Category', category), *git_blame(file_name, lineno))

def file_matcher(file_name):
	blacklist = ('gnuradio_swig_py_general.cc', 'Makefile.in')
	if file_name in blacklist: return False
	return re.compile('^((\w*\.)*(m4|am|in|ac|py|c|cc|i|h|t|v|common))$').match(file_name)

if __name__ == '__main__':
	#setup the option parser
	parser = optparse.OptionParser()
	parser.add_option("--src-dir", type="string", default=None)
	parser.add_option("--html-dir", type="string", default='html')
	(options, args) = parser.parse_args()

	#setup the kludge tracker parser
	ktp = kludgetracker.parser()
	ktp.register_matcher(pyflakes_matcher)
	ktp.register_matcher(re_line_matcher)

	#parse and generate
	files = kludgetracker.get_matching_files(options.src_dir, file_matcher)
	result = ktp(files, path=os.path.dirname(os.path.abspath(options.src_dir)))
	desc = git_command(options.src_dir, 'describe')
	gen = kludgetracker.generator(result, title='Gnuradio - %s'%desc)
	gen.generate(options.html_dir)
	print 'Done'
