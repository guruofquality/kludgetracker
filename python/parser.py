import os

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
	def __init__(self, file, lines, lineno, matcher):
		self._file = file
		self._lines = lines
		self._lineno = lineno
		self._matcher = matcher

	def get_file(self): return self._file
	def get_lines(self): return self._lines
	def get_lineno(self): return self._lineno
	def get_category(self): return self._matcher.get_category()

class _result(object):
	"""
	A result of a parsing.
	"""
	def __init__(self, chunks): self._chunks = chunks

	def get_chunks(self, files=None, categories=None):
		if files is None: files = self.get_files()
		if categories is None: categories = self.get_categories()
		def is_match(chunk): return \
			chunk.get_file() in files or \
			chunk.get_category() in categories
		return filter(is_match, self._chunks)

	def get_files(self): return set(map(_chunk.get_file, self._chunks))
	def get_categories(self): return set(map(_chunk.get_category, self._chunks))

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
		chunks = list()
		for file in files:
			lines = open(file, 'r').readlines()
			for matcher in self._matchers:
				for i, line in enumerate(lines):
					if matcher(line): chunks.append(_chunk(
						file = os.path.relpath(file, path),
						lines = lines,
						lineno = i,
						matcher = matcher,
					))
		return _result(chunks)
