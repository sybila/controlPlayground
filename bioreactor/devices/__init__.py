modules = [".GMS", ".GAS", ".PBR", ".PBR_test"]

for module in modules:
	exec("from " + module + " import *")