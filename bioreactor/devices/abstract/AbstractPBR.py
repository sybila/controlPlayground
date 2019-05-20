from .device import Device

# Abstract Bioreactor
class AbstractPBR(Device):
    def __init__(self, particle, ID, adress):
        super(AbstractPBR, self).__init__(particle, ID, adress)

    def id(self):
        raise NotImplementedError("The method not implemented")

    def get_temp_settings(self):
        '''
        Get information about currently set temperature, maximal and
        minimal allowed temperature.

        Returns:
            dict: The current settings structured in a dictionary.
        '''
        raise NotImplementedError("The method not implemented")

    def get_temp(self):
        '''
        Get current temperature in Celsius degree.

        Returns:
            float: The current temperature.
        '''
        raise NotImplementedError("The method not implemented")

    def set_temp(self, temp):
        '''
        Set desired temperature in Celsius degree.

        Args:
            temp (float): The temperature.
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

    def get_ph(self):
        '''
        Get current pH (dimensionless.)

        Returns:
            float: The current pH.
        '''
        raise NotImplementedError("The method not implemented")

    def measure_od(self, channel=0):
        '''
        Measure current Optical Density (OD, dimensionless).

        Returns:
            integer: Measured OD
        '''
        raise NotImplementedError("The method not implemented")

    def get_pump_params(self, pump):
        '''
        Get parameters for given pump.

        Args:
            pump (int): Given pump
        Returns:
            dict: The current settings structured in a dictionary.
        '''
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

    def set_pump_state(self, pump, on):
        '''
        Turns on/off given pump.

        Args:
            pump (int): ID of a pump
            on (bool): True to turn on, False to turn off
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

    def set_light_intensity(self, channel, intensity):
        '''
        Control LED panel on photobioreactor.

        Args:
            channel (int): Given channel (0 for red light, 1 for blue light)
            intensity (float): Desired intensity
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

    def turn_on_light(self, channel, on):
        '''
        Turn on/off LED panel on photobioreactor.

        Args:
            channel (int): Given channel
            on (bool): True turns on, False turns off
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

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
        raise NotImplementedError("The method not implemented")

    def set_thermoregulator_state(self, on):
        '''
        Set state of thermoregulator.

        Args:
            on (int): 1 -> on, 0 -> freeze, -1 -> off
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")
