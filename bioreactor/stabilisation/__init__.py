modules = [".DataHolder", ".GrowthChecker", ".Regression", ".Stabiliser"]

for module in modules:
    exec("from " + module + " import *")
