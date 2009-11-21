import os
import utils
import pickle
import tempfile

class _matcher(object):
	"""
	Hold a matcher function and its associated information.
	"""
	def __init__(self, matcher, category='default'):
		self._matcher = matcher
		self._category = category

	def get_category(self): return self._category
	def __call__(self, *args): return self._matcher(*args)

class _chunk(object):
	"""
	A single line with a todofixme and its associated information.
	"""
	def __init__(self, file, lines, lineno, category):
		self._file = file
		self._lines = lines
		self._lineno = lineno
		self._category = category

	def get_file(self): return self._file
	def get_lines(self): return self._lines
	def get_lineno(self): return self._lineno
	def get_category(self): return self._category

class _result(object):
	"""
	A result of a parsing.
	"""
	def __init__(self, chunks): self._chunks = chunks

	def get_subset(self, files=None, categories=None, subdir=None):
		def is_match(chunk):
			if files is not None and chunk.get_file() in files: return True
			if categories is not None and chunk.get_category() in categories: return True
			if subdir is not None:
				dirname = os.path.dirname(chunk.get_file())
				if dirname:
					reldir = os.path.relpath(dirname, subdir)
					if '..' not in reldir: return True
			return False
		return _result(filter(is_match, self._chunks))

	def __len__(self): return len(self.get_chunks())
	def get_chunks(self): return self._chunks
	def get_files(self): return set(map(_chunk.get_file, self.get_chunks()))
	def get_categories(self): return set(map(_chunk.get_category, self.get_chunks()))
	def get_subdirs(self):
		subdirs = set()
		for subdir in set(map(os.path.dirname, self.get_files())):
			while subdir:
				subdirs.add(subdir)
				subdir = os.path.dirname(subdir)
		return subdirs

class parser(object):
	"""
	A collection of matchers.
	"""
	def __init__(self):
		self._matchers = list()

	def register_matcher(self, *args, **kwargs):
		"""
		Register a new matcher function.
		@param matcher a function that takes a string and returns true/false
		"""
		self._matchers.append(_matcher(*args, **kwargs))

	def __call__(self, files, path='/'):
		num_procs = utils.get_num_procs()
		tmpfiles = [tempfile.mkstemp()[1] for num in range(num_procs)]
		for num in range(num_procs):
			if os.fork(): continue
			chunks = list()
			for file in files[num::num_procs]:
				print 'Parsing:', os.path.abspath(file)
				lines = open(file, 'r').readlines()
				for matcher in self._matchers:
					for i, line in enumerate(lines):
						if matcher(line): chunks.append(_chunk(
							file = os.path.relpath(file, path),
							lines = lines,
							lineno = i,
							category = matcher.get_category(),
						))
			pickle.dump(chunks, open(tmpfiles[num], 'wb'))
			exit()
		for num in range(num_procs): os.wait()
		return _result(sum([pickle.load(open(tmpfile, 'rb')) for tmpfile in tmpfiles], []))
