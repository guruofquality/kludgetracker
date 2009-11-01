#!/usr/bin/env python

import re
import todofixme

parser = todofixme.parser()
parser.register_matcher(re.compile('(?i).*(todo|fixme|magic|kludge).*').match)

for chunk in parser.get_chunks('test.txt'):
	print chunk.get_lineno(), chunk.get_lines()[chunk.get_lineno()]
