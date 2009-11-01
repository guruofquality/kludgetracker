#todo
#fixme
#magic
#kludge

class matcher(object):
	"""
	Hold a matcher function and its associated information.
	"""
	def __init__(matcher, category='default'):
		self._matcher = matcher
		self._category = category

	def get_category(self): return self._category
	def __call__(self, *args): return self._matcher(*args)

class _chunk(object):
	"""
	A single line with a todofixme and its associated information.
	"""
	def __init__(self, lines, lineno, matcher):
		self._lines = lines
		self._lineno = lineno
		self._matcher = matcher

	def get_lines(self): return self._lines
	def get_lineno(self): return self._lineno
	def get_category(self): return self._matcher.get_category()

class parser(object):
	"""
	A collection of matchers.
	"""
	def __init__(self):
		self._matchers = list()

	def register_matcher(self, matcher):
		"""
		Register a new matcher function.
		@param matcher a function that takes a string and returns true/false
		"""
		self._matchers.append(matcher)

	def get_chunks(self, file):
		chunks = list()
		lines = open(file, 'r').readlines()
		for matcher in self._matchers:
			for i, line in enumerate(lines):
				if matcher(line): chunks.append(_chunk(
					lines = lines,
					lineno = i,
					matcher = matcher,
				))
		return chunks
