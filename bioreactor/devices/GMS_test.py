from .abstract import AbstractGMS

# Gas Mixer
class GMS_test(AbstractGMS):
    def __init__(self, particle, ID, adress):
        super(GMS_test, self).__init__(particle, ID, adress)
        self.GAS_TYPES = ["CO2", "Air", "N2"]

    def get_valve_flow(self, valve):
        '''
        Get value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: The current settings of the valve flow and actual value, both in (L/min).
        '''
        return {"current": 5, "set": 10}

    def set_valve_flow(self, valve, value):
        '''
        Set value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
            value (float): desired value for valve flow in (L/min).
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        return True

    def get_valve_info(self, valve):
        '''
        Gives information about the valve

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: A dictionary with gas type and maximal allowed flow.
        '''
        return {"max_flow": 10, "gas_type": self.GAS_TYPES[0]}

