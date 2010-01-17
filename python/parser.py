import os
import utils
import multiprocessing

class _chunk(object):
	"""
	A single line with a todofixme and its associated information.
	"""
	def __init__(self, file, lines, lineno, info):
		self._file = file
		self._lines = lines
		self._lineno = lineno
		self._info = info

	def get_file(self): return self._file
	def get_lines(self): return self._lines
	def get_lineno(self): return self._lineno
	def get_info(self): return self._info

class _result(object):
	"""
	A result of a parsing.
	"""
	def __init__(self, chunks): self._chunks = chunks

	def get_subset(self, files=None, subdir=None):
		def is_match(chunk):
			if files is not None and chunk.get_file() in files: return True
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

	def register_matcher(self, matcher):
		"""
		Register a new matcher function.

		A matcher is a function that takes two arguments:
			1) a file path
			2) a callable handler

		The matcher should call the handler for each match,
		passing the line number as the first argument.
		All proceeding arguments are optional (key, value) tuples
		that provide additional info or meta-data about the match.

		The line numbering starts at index 0 for the first line.
		"""
		self._matchers.append(matcher)

	def _get_chunks(self, files, path):
		chunks = list()
		#create a new handler callback
		def handler(lineno, *info):
			chunks.append(_chunk(
				file = os.path.relpath(file, path),
				lines = lines,
				lineno = lineno,
				info = info,
			))
		#call every matcher on every file
		for file in files:
			print 'Parsing:', os.path.abspath(file)
			lines = open(file, 'r').readlines()
			#call each matcher with the handler
			for matcher in self._matchers:
				matcher(file, handler)
		return chunks

	def __call__(self, files, path='/'):
		num_procs = utils.get_num_procs()
		chunks = multiprocessing.Manager().list()
		procs = [multiprocessing.Process(
			target=lambda *files: chunks.extend(
				self._get_chunks(files=files, path=path)),
			args=files[num::num_procs],
		) for num in range(num_procs)]
		map(multiprocessing.Process.start, procs)
		map(multiprocessing.Process.join, procs)
		return _result(list(chunks))
