from .device import Device

# Gas Mixer
class GMS(Device):
    def __init__(self, particle, ID, adress):
        super(GMS, self).__init__(particle, ID, adress)
        self.GAS_TYPES = ["CO2", "Air", "N2"]

    def get_valve_flow(self, valve):
        '''
        Get value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: The current settings of the valve flow and actual value, both in (L/min).
        '''
        results = ["current", "set"]
        try:
            values = self.parent.execute(self, "get-valve-flow", [valve])[0].rstrip()[1:-1].split()
        except Exception:
            return None
        return dict(zip(results, list(map(float, values[1:-1]))))
        '''
        Set flow to value for the given valve.
        '''
    def set_valve_flow(self, valve, value):
        '''
        Set value (L/min) of current flow in the given valve.

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
            value (float): desired value for valve flow in (L/min).
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        try:
            return self.parent.execute(self, "set-valve-tflow", [valve, value])[0].rstrip() == 'ok'
        except Exception:
            return None

    def get_valve_info(self, valve):
        '''
        Gives information about the valve

        Args:
            valve (int): ID of the valve (0 for CO2, 1 for Air)
        Returns:
            dict: A dictionary with gas type and maximal allowed flow.
        '''
        results = ["max_flow", "gas_type"]
        values = [None, None]
        try:
            values = self.parent.execute(self, "get-valve-info", [valve])[0].rstrip()[1:-1].split()
        except Exception:
            return None
        return dict(zip(results, [float(values[1]), self.GAS_TYPES[int(values[3])]]))

