import os
import multiprocessing

def get_num_procs(): # the famous N+1 heuristic
	return multiprocessing.cpu_count() + 1

def get_matching_files(path, matcher):
	path = os.path.abspath(path)
	files = list()
	for file in os.listdir(path):
		subpath = os.path.join(path, file)
		if os.path.isfile(subpath) and matcher(file):
			files.append(os.path.abspath(subpath))
		if os.path.isdir(subpath):
			files.extend(get_matching_files(subpath, matcher))
	return files
