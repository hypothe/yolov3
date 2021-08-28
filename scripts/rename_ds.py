import os
import re
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--dir', type=str, default='', help='directory path', required=True)
	opt = parser.parse_args()

	assert os.path.isdir(opt.dir), "ERROR: directory %s not found" % opt.dir

	files = os.listdir(opt.dir)

	for file in files:
		last_dot = file.rfind('.')
		assert last_dot > 0, "ERROR: in file name %s" % file
		subname = file[0:last_dot]
		undotted_file = re.sub(r'\.', '_', subname) + file[last_dot:]

		os.rename(os.path.join(opt.dir, file), os.path.join(opt.dir, undotted_file))

if __name__ == '__main__':
	main()