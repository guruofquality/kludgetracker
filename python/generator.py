import os
import utils
import multiprocessing
import Cheetah.Compiler

this_dir = os.path.dirname(__file__)

class Template(object):
	def __init__(self, file):
		ns = dict() #namespace dict
		module_name = '__compiled_template__'
		exec(str(Cheetah.Compiler.Compiler(file=file, moduleName=module_name)), ns)
		self._template = ns[module_name]
	def parse(self, **args):
		return str(self._template(searchList=args))

class generator(object):
	def __init__(self, result, title='work'):
		self._result = result
		self._title = title

	def _generate_subdirs(self, subdirs, gen_dir, template):
		for subdir in subdirs:
			#ensure that the directory exists
			dir = os.path.join(gen_dir, subdir)
			if not os.path.exists(dir):
				#could fail if another process also did makedirs
				try: os.makedirs(dir)
				except: pass
			#generate the html file
			html_file = os.path.abspath(os.path.join(dir, 'index.html'))
			print 'Generating:', html_file
			html_str = template.parse(
				title='Kludge Tracker: %s'%self._title,
				result=self._result.get_subset(subdir=subdir),
				rel_dir=subdir,
			)
			open(html_file, 'w').write(html_str)

	def generate(self, gen_dir='html',
		style_sheet_file=os.path.join(this_dir, 'style.css'),
		index_tmpl_file=os.path.join(this_dir, 'index.tmpl'),
	):
		index_tmpl = Template(index_tmpl_file)
		num_procs = utils.get_num_procs()
		subdirs = sorted(self._result.get_subdirs())
		#generate html for each subdirectory
		procs = [multiprocessing.Process(
			target=lambda *subdirs: self._generate_subdirs(
				subdirs=subdirs, gen_dir=gen_dir, template=index_tmpl),
			args=subdirs[num::num_procs],
		) for num in range(num_procs)]
		map(multiprocessing.Process.start, procs)
		map(multiprocessing.Process.join, procs)
		#copy in style sheet
		css_file = os.path.abspath(os.path.join(gen_dir, 'style.css'))
		print "Generating:", css_file
		open(css_file, 'w').write(Template(style_sheet_file).parse())

