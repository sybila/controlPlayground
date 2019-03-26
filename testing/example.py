import os, sys

workspace = os.path.dirname(__file__)
sys.path.append(os.path.join(workspace, '../'))
import bioreactor

node = bioreactor.Node('root', '/root/control/', '192.168.17.13')
node.add_device("PBR", "PBR07", 72700007)
node.add_device("GMS", "GMS", 46700003)
node.add_device("GAS", "GAS", 42700007)

print(node.devices)
print(node.PBR.get_temp())