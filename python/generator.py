from Cheetah import Template as _Template
def Template(_tmpl_str, **kwargs):
	return str(_Template.Template(_tmpl_str, kwargs))

import os

this_dir = os.path.dirname(__file__)

class generator(object):
	def __init__(self, result, title='work'):
		self._result = result
		self._title = title

	def generate(self, gen_dir='html',
		style_sheet=os.path.join(this_dir, 'style.css'),
		index_tmpl=os.path.join(this_dir, 'index.tmpl'),
		):
		result = self._result

		tmpl_str = open(index_tmpl, 'r').read()
		#generate html for each subdirectory
		for subdir in sorted(result.get_subdirs()):
			html_file = os.path.join(gen_dir, subdir, 'index.html')
			try: os.makedirs(os.path.dirname(html_file))
			except: pass
			print 'Generating:', html_file
			open(html_file, 'w').write(Template(tmpl_str,
				title='Kludge Tracker: %s'%self._title,
				result=result.get_subset(subdir=subdir),
				rel_dir=subdir,
			))

		#copy in style sheet
		css_str = open(style_sheet, 'r').read()
		open(os.path.join(gen_dir, 'style.css'), 'w').write(css_str)

