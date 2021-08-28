import argparse
import yaml
import re
import os

if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument('--cfg', type=str, default='../cfg/yolor_p6.cfg', help='model.yaml path')
		parser.add_argument('--custom-cfg', type=str, default='../cfg/yolor_p6_custom.cfg', help='custom_model.yaml path')
		parser.add_argument('--data', type=str, default='../data/coco.yaml', help='data.yaml path')

		
		opt = parser.parse_args()

		assert os.path.isfile(opt.cfg), "ERROR: cfg not %s found" % opt.cfg
		assert os.path.isfile(opt.data), "ERROR: data not %s found" % opt.data

		with open(opt.data, "r") as f:
			dataMap = yaml.safe_load(f)

		num_classes = len(dataMap['names'])
		#str_clsses = "classes=" + num_classes
		num_filters = (num_classes + 5) * 3
		#str_filters = "filters=" + num_filters

		custom_cfg_str=""

		with open(opt.cfg, "r") as f:
			for line in f:
				strl = line.strip()
				#print(strl)
				strl = re.sub(r'(?<=filters=)\d+', str(num_filters), strl)
				strl = re.sub(r'(?<=classes=)\d+', str(num_classes), strl)
				custom_cfg_str += strl + "\n"

			with open(opt.custom_cfg, "w") as f:
				f.write(custom_cfg_str)
