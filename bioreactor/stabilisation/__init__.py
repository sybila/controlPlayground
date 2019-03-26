modules = [".DataHolder", ".GrowthChecker", ".Regression", ".OD_stabilisation"]

for module in modules:
	exec("from " + module + " import *")