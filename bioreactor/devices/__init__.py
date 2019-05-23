modules = [".GMS", ".GAS", ".PBR", ".PBR_test", ".GMS_test"]

for module in modules:
    exec("from " + module + " import *")
