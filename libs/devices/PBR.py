from device import Device
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
