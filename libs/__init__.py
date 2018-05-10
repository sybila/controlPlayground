modules = ["progress"]

for module in modules:
	exec("from " + module + " import *")