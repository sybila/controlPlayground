from .device import Device
from math import log10
import random

# Fake bioreactor
class PBR_test(Device):
    def __init__(self, particle, ID, adress):
        super(PBR_test, self).__init__(particle, ID, adress)
        self.last_value = 0.45
        self.increasing = False

    def id(self):
        return "(" + self.ID + ")"

    def get_temp_settings(self):
        return {"set": 25, "min": 10, "max": 35}

    def get_temp(self):
        return 25

    def set_temp(self, temp):
        return True

    def get_ph(self):
        return 7

    def measure_od(self, channel=0):
        step = 0.002
        sign = 1 if self.increasing else -1
        if random.random() < 0.05:
            step = random.random()
            if random.random() > 0.001:
                return self.last_value + sign * step
        self.last_value += sign * step
        return self.last_value

    def get_pump_params(self, pump):
        return {"direction": 1, "on": True, "valves": 10,
                    "flow": 0.3, "min": 0, "max": 100}

    def set_pump_params(self, pump, direction, flow):
        return True

    def set_pump_state(self, pump, on):
        self.increasing = not bool(on)
        return True

    def get_light_intensity(self, channel):
        return {"intensity": 500, "max": 1000, "on": true}

    def set_light_intensity(self, channel, intensity):
        return True

    def turn_on_light(self, channel, on):
        return True

    def get_pwm_settings(self):
        return {"pulse": 1, "min": 0, "max": 100, "on": True}

    def set_pwm(self, value, on):
        return True

    def get_o2(self, raw=True, repeats=5, wait=0):
        return 10

def to_scheme_bool(value):
    return "#t" if value else "#f" 

def from_scheme_bool(value):
    return True if value == "#t" else False

# fake SSH connection
class SSHconnection():
    def __init__(self, server, user):
        pass

    def disconnect(self):
        return 
