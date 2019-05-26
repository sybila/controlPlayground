from .encoder import *
from .decoder import *


def write_xml(settings_dict, working_dir):
    obj = Dict2XML()
    with open(working_dir + "/settings.xml", "w") as text_file:
        result = obj.parse(settings_dict)
        text_file.write(result)


def read_xml(filename):
    obj = XML2Dict()
    return obj.parse(filename)
