from math import log10
from .abstract import AbstractPBR


# Bioreactor
class PBR(AbstractPBR):
    def __init__(self, particle, ID, adress):
        super(PBR, self).__init__(particle, ID, adress)

    def id(self):
        return "(" + self.ID + ")"

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
        except Exception as e:
            print(self.id(), e)
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
        except Exception as e:
            print(self.id(), e)
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
        except Exception as e:
            print(self.id(), e)
            return False

    def get_ph(self):
        '''
        Get current pH (dimensionless.)

        Returns:
            float: The current pH.
        '''
        try:
            return float(self.parent.execute(self, "get-ph", [5, 0])[0])
        except Exception as e:
            print(self.id(), e)
            return None

    def measure_od(self, channel=0):
        '''
        Measure current Optical Density (OD, dimensionless).

        Returns:
            integer: Measured OD
        '''
        result = self.parent.execute(self, "measure-od", [channel, 30])[0].rstrip().split()
        return -log10((int(result[1]) - int(result[2][:-1])) / 40000)

    def get_pump_params(self, pump):
        '''
        Get parameters for given pump.

        Args:
            pump (int): Given pump
        Returns:
            dict: The current settings structured in a dictionary.
        '''

        try:
            result = self.parent.execute(self, "get-pump-info", [pump])[0].rstrip()[1:-1].split()
            return {"direction": int(result[1]), "on": from_scheme_bool(result[2]), "valves": int(result[3]),
                    "flow": float(result[4]), "min": float(result[5]), "max": float(result[6])}
        except Exception as e:
            print(self.id(), e)
            return False

    def set_pump_params(self, pump, direction, flow):
        '''
        Set up the rotation direction and flow for given pump.

        Args:
            pump (int): Given pump
            rotation_direction (int): Rotation direction (1 right, -1 left)
            flow (float): Desired flow rate
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-pump-params", [pump, direction, flow])[0].rstrip() == 'ok'
        except Exception as e:
            print(self.id(), e)
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
        except Exception as e:
            print(self.id(), e)
            return False

    def get_light_intensity(self, channel):
        '''
        Checks for current (max?) light intensity.

        Args:
            channel (int): Given channel ID
        Returns:
            dict: The current settings structured in a dictionary.
            
        Items: "intensity": current light intensity (float) in μE, 
            "max": maximal intensity (float) in μE, 
            "on": True if light is turned on (bool)
        '''

        try:
            result = self.parent.execute(self, "get-actinic-continual-settings", [channel])[0].rstrip()[1:-1].split()
            return {"intensity": float(result[1]), "max": float(result[2]), "on": from_scheme_bool(result[3])}
        except Exception as e:
            print(self.id(), e)
            return None

    def set_light_intensity(self, channel, intensity):
        '''
        Control LED panel on photobioreactor.

        Args:
            channel (int): Given channel (0 for red light, 1 for blue light)
            intensity (float): Desired intensity
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-actinic-continual-intensity", [channel, intensity])[
                       0].rstrip() == 'ok'
        except Exception as e:
            print(self.id(), e)
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
            return self.parent.execute(self, "set-actinic-continual-mode", [channel, to_scheme_bool(on)])[
                       0].rstrip() == 'ok'
        except Exception as e:
            print(self.id(), e)
            return False

    def get_pwm_settings(self):
        '''
        Checks for current stirring settings.

        Returns:
            dict: The current settings structured in a dictionary.
            
        Items: "pulse": current stirring in %, 
            "min": minimal stirring in %, 
            "max": maximal stirring in %,
            "on": True if stirring is turned on (bool)
        '''
        try:
            result = self.parent.execute(self, "get-pwm-settings")[0].rstrip()[1:-1].split()
            return {"pulse": result[1], "min": result[2],
                    "max": result[3], "on": from_scheme_bool(result[4])}
        except Exception as e:
            print(self.id(), e)
            return False

    def set_pwm(self, value, on):
        '''
        Set stirring settings.
        Channel: 0 je red and 1 blue according to PBR configuration.

        Args:
            value (int): desired stirring pulse
            on (bool): True turns on, False turns off
        Returns:
            bool: True if was succesful, False otherwise.
        '''

        try:
            return self.parent.execute(self, "set-pwm", [value, to_scheme_bool(on)])[0].rstrip() == 'ok'
        except Exception as e:
            print(self.id(), e)
            return False

    def get_o2(self, raw=True, repeats=5, wait=0):
        '''
        Checks fr concentration of dissociated O2.

        Returns:
            dict: The current settings structured in a dictionary.
            
        Items: "pulse": current stirring in %, 
            "min": minimal stirring in %, 
            "max": maximal stirring in %,
            "on": True if stirring is turned on (bool)
        '''
        try:
            return float(self.parent.execute(self, "get-o2/h2", [repeats, wait, to_scheme_bool(raw)])[0].rstrip())
        except Exception as e:
            print(self.id(), e)
            return False

    def get_thermoregulator_settings(self):
        '''
        Get current settings of thermoregulator.

        Returns:
            dict: The current settings structured in a dictionary.
            
        Items: "temp": current temperature in Celsius degrees, 
            "min": minimal allowed temperature, 
            "max": maximal allowed temperature,
            "on": state of thermoregulator (1 -> on, 0 -> freeze, -1 -> off)
        '''
        try:
            result = self.parent.execute(self, "get-thermoregulator-settings")[0].rstrip()[1:-1].split()
            return {"temp": float(result[1]), "min": float(result[2]),
                    "max": float(result[3]), "on": int(result[4])}
        except Exception as e:
            print(self.id(), e)
            return False

    def set_thermoregulator_state(self, on):
        '''
        Set state of thermoregulator.

        Args:
            on (int): 1 -> on, 0 -> freeze, -1 -> off
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        try:
            return self.parent.execute(self, "set-thermoregulator-state", [on])[0].rstrip() == 'ok'
        except Exception as e:
            print(self.id(), e)
            return False

    def measure_ft(self, channel):
        '''
        ???

        Args:
            channel (int): ???
        Returns:
            ???: ???
        '''
        try:
            return float(self.parent.execute(self, "measure-ft", [channel])[0].rstrip())
        except Exception as e:
            return None


def to_scheme_bool(value):
    return "#t" if value else "#f"


def from_scheme_bool(value):
    return True if value == "#t" else False
