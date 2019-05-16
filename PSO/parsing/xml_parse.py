import encoder
import decoder

def write_xml(settings_dict):
	obj = decoder.Dict2XML()
	print(obj.parse(settings_dict))

def read_xml(filename):
	tree = ET.parse(filename)
	root = tree.getroot()