modules = ["GMS", "GAS", "PBR"]

for module in modules:
	exec("from " + module + " import *")