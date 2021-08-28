import argparse
import yaml
import re
import os

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--cfg', type=str, default='../cfg/yolor_p6.cfg', help='model.yaml path')
	parser.add_argument('--custom-cfg', type=str, default='../cfg/yolor_p6_custom.cfg', help='custom_model.yaml path')
	parser.add_argument('--data', type=str, default='../data/coco.yaml', help='data.yaml path')
	parser.add_argument('--legacy-data', type=str, default='', help='output name of the legacy data file generated (leave empty for none)')

	
	opt = parser.parse_args()

	assert os.path.isfile(opt.cfg), "ERROR: cfg not %s found" % opt.cfg
	assert os.path.isfile(opt.data), "ERROR: data not %s found" % opt.data

	with open(opt.data, "r") as f:
		dataMap = yaml.safe_load(f)

	num_classes = len(dataMap['names'])
	#str_clsses = "classes=" + num_classes
	num_filters = (num_classes + 5) * 3
	#str_filters = "filters=" + num_filters
	max_batches = 2000*num_classes

	custom_cfg_str=""

	with open(opt.cfg, "r") as f:
		for line in f:
			strl = line.strip()
			#print(strl)
			strl = re.sub(r'(?<=filters=)\d+(?=\s*activation=linear)', str(num_filters), strl)
			strl = re.sub(r'(?<=classes=)\d+', str(num_classes), strl)
			strl = re.sub(r'(?<=max_batches=)\d+', str(max_batches), strl)
			strl = re.sub(r'(?<=steps=)\d+,\d+', str(0.8*max_batches)+str(0.9*max_batches), strl)
			custom_cfg_str += strl + "\n"

		with open(opt.custom_cfg, "w") as f:
			f.write(custom_cfg_str)

	if opt.legacy_data:
		# generate a file listing the class names
		names_file = re.sub(r'\.yaml', '.names', opt.legacy_data)
		with open(names_file, "w") as f:
			for name in dataMap['names']:
				f.write("%s\n" % name)
		# generate the legacy version of the data file,
		# needed by yolov3-archive
		with open(opt.legacy_data, "w") as f:
			f.write("classes=%d\n" % num_classes)
			f.write("train=%s\n" % dataMap['train'])
			f.write("valid=%s\n" % dataMap['val'])
			f.write("names=%s\n" % names_file)