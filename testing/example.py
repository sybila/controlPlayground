import os, sys
import time

workspace = os.path.dirname(__file__)
sys.path.append(os.path.join(workspace, '../'))
import bioreactor

node = bioreactor.Node('root', '/root/control/', '192.168.17.13')
node.add_device("PBR", "PBR07", 72700007)
node.add_device("GMS", "GMS", 46700003)
node.add_device("GAS", "GAS", 42700007)

print(node.devices)
print(node.PBR.get_temp())
print(node.PBR.get_pump_params(5))
print(node.PBR.get_pwm_settings())
print(node.PBR.set_pwm(50, True))
print(node.PBR.get_pwm_settings())
time.sleep(1)
print(node.PBR.set_pwm(50, False))
print(node.PBR.get_pwm_settings())

#print(node.PBR.get_light_intensity(0))
#print(node.PBR.turn_on_light(0, True))