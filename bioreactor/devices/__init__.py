# for testing with Fake Bioreactor
modules = [".GMS", ".GAS", ".PBR_test"]
# modules = [".GMS", ".GAS", ".PBR"]

for module in modules:
	exec("from " + module + " import *")