from Cheetah import Template as _Template
def Template(_tmpl_str, **kwargs):
	return str(_Template.Template(_tmpl_str, kwargs))

import os
import utils

this_dir = os.path.dirname(__file__)

class generator(object):
	def __init__(self, result, title='work'):
		self._result = result
		self._title = title

	def generate(self, gen_dir='html',
		style_sheet=os.path.join(this_dir, 'style.css'),
		index_tmpl=os.path.join(this_dir, 'index.tmpl'),
	):
		num_procs = utils.get_num_procs()
		subdirs = sorted(self._result.get_subdirs())

		#create all directories
		for subdir in subdirs:
			try: os.makedirs(os.path.join(gen_dir, subdir))
			except: pass

		#generate html for each subdirectory
		tmpl_str = open(index_tmpl, 'r').read()
		for num in range(num_procs):
			if os.fork(): continue
			for subdir in subdirs[num::num_procs]:
				html_file = os.path.abspath(os.path.join(gen_dir, subdir, 'index.html'))
				print 'Generating:', html_file
				html_str = Template(tmpl_str,
					title='Kludge Tracker: %s'%self._title,
					result=self._result.get_subset(subdir=subdir),
					rel_dir=subdir,
				)
				open(html_file, 'w').write(html_str)
			exit()
		for num in range(num_procs): os.wait()

		#copy in style sheet
		css_file = os.path.abspath(os.path.join(gen_dir, 'style.css'))
		print "Generating:", css_file
		css_str = open(style_sheet, 'r').read()
		open(css_file, 'w').write(css_str)

		print 'Done'

