from .device import Device


# Abstract Gas Mixer
class AbstractGMS(Device):
    def __init__(self, particle, ID, adress):
        super(AbstractGMS, self).__init__(particle, ID, adress)

    def get_valve_flow(self, valve):
        '''
        Get value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: The current settings of the valve flow and actual value, both in (L/min).
        '''
        raise NotImplementedError("The method not implemented")

    def set_valve_flow(self, valve, value):
        '''
        Set value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
            value (float): desired value for valve flow in (L/min).
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

    def get_valve_info(self, valve):
        '''
        Gives information about the valve

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: A dictionary with gas type and maximal allowed flow.
        '''
        raise NotImplementedError("The method not implemented")
