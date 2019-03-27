from .device import Device
from math import log10

# Bioreactor
class PBR(Device):
    def __init__(self, particle, ID, adress):
        super(PBR, self).__init__(particle, ID, adress)

    def get_temp_settings(self):
        '''
        Get information about currently set temperature, maximal and
        minimal allowed temperature.

        Returns:
            dict: The current settings structured in a dictionary.
        '''
        results = ["set", "min", "max"]
        try:
            values = self.parent.execute(self, "get-thermoregulator-settings")[0].rstrip()[1:-1].split()
        except Exception:
            return None
        return dict(zip(results, list(map(float, values[1:-1]))))

    def get_temp(self):
        '''
        Get current temperature in Celsius degree.

        Returns:
            float: The current temperature.
        '''
        try:
            return float(self.parent.execute(self, "get-current-temperature")[0])
        except Exception:
            return None

    def set_temp(self, temp):
        '''
        Set desired temperature in Celsius degree.

        Args:
            temp (float): The temperature.
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        try:
            return self.parent.execute(self, "set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
        except Exception:
            return False

    def get_ph(self):
        '''
        Get current pH (dimensionless.)

        Returns:
            float: The current pH.
        '''
        try:
            return float(self.parent.execute(self, "get-ph", [5, 0])[0])
        except Exception:
            return None

    def measure_od(self):
        '''
        Measure current Optical Density (OD, dimensionless).

        Returns:
            integer: Measured OD
        '''
        try:
            result = self.parent.execute(self, "measure-od", [0, 5])[0].rstrip().split()
            return -log10((int(result[1]) - int(result[2][:-1]))/100000)
        except Exception:
            return None

    def set_pump_params(self, pump, direction, flow):
        '''
        Set up the ratation direction and flow for given pump.

        Args:
            pump (int): Given pump
            rotation_direction (?): Rotation direction
            flow (float): Desired flow rate
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-pump-params", [pump, direction, flow])[0].rstrip() == 'ok'
        except Exception:
            return False

    def set_pump_state(self, pump, on):
        '''
        Turns on/off given pump.

        Args:
            pump (int): ID of a pump
            on (bool): True to turn on, False to turn off
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-pump-state", [pump, to_scheme_bool(on)])[0].rstrip() == 'ok'
        except Exception:
            return False

    def get_light_intensity(self, channel):
        '''
        Checks for current (max?) light intensity.

        Args:
            channel (int): Given channel ID
        Returns:
            float: current light intensity in μE
        '''

        try:
            return float(self.parent.execute(self, "get-actinic-continual-settings", [channel])[0])
        except Exception:
            return None

    def set_light_intensity(self, channel, intensity):
        '''
        Control LED panel on photobioreactor.
        Channel: 0 je red/white and 1 blue/red according to PBR configuration.

        Args:
            channel (int): Given channel
            intensity (float): Desired intensity
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-actinic-continual-intensity", [channel, intensity])[0].rstrip() == 'ok'
        except Exception:
            return False

    def turn_on_light(self, channel, on):
        '''
        Turn on/off LED panel on photobioreactor.

        Args:
            channel (int): Given channel
            on (bool): True turns on, False turns off
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-actinic-continual-mode", [to_scheme_bool(on)])[0].rstrip() == 'ok'
        except Exception:
            return False


def to_scheme_bool(value):
    return "#t" if values else "#f" 