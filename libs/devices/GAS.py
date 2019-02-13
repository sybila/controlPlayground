from device import Device

# Gas Analyser
class GAS(Device):
    def __init__(self, particle, ID, adress):
        super(GAS, self).__init__(particle, ID, adress)

    def get_co2_air(self):
        '''
        TBA
        '''
        try:
            return float(self.parent.execute(self, "get-co2-air")[0].rstrip())
        except Exception:
            return None

    def get_small_valves(self):
        '''
        Obtain settings of individual vents of GAS device.

        Represented as one byte, where first 6 bits represent 
        vents indexed as in a picture scheme available here: 
        https://i.imgur.com/jSeFFaO.jpg

        Returns:
            string: byte representation of vents settings.
        '''
        try:
            value = int(self.parent.execute(self, "get-small-valves")[0].rstrip())
        except Exception:
            return None
        return bin(value)[2:]

    def set_small_valves(self, mode):
        '''
        Changes settings of individual vents of GAS device.

        Can be set by one byte (converted to int), where first 6
        bits represent vents indexed as in a picture scheme
        available here: https://i.imgur.com/jSeFFaO.jpg

        Mode 0 - normal mode, output from GMS goes to PBR
        Mode 1 - reset mode, N2 (nitrogen) goes to PBR

        Args:
            mode (int): chosen mode (0 or 1)
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        modes = {0 : "11111111", 1 : "11101111"}
        try:
            return self.parent.execute(self, "set-small-valves", [int(modes[mode], 2)])[0].rstrip() == 'ok'
        except Exception:
            return None

    def get_flow(self):
        '''
        Actual flow being send from GAS to the PBR.

        Returns:
            float: The current flow in L/min.
        '''
        try:
            return float(self.parent.execute(self, "get-flow", [1])[0].rstrip())
        except Exception:
            return None

    def get_flow_target(self):
        '''
        Actual desired flow.

        Returns:
            float: The desired flow in L/min.
        '''
        try:
            return float(self.parent.execute(self, "get-flow-target")[0].rstrip())
        except Exception:
            return None

    def set_flow_target(self, flow):
        '''
        Set flow we want to achieve.

        Args:
            flow (float): flow in L/min we want to achieve (max given by get_flow_max)
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        try:
            return self.parent.execute(self, "set-flow-target", [flow])[0].rstrip() == 'ok'
        except Exception:
            return None

    def get_flow_max(self):
        '''
        Maximal allowed flow.

        Returns:
            float: The maximal flow in L/min
        '''
        try:
            return float(self.parent.execute(self, "get-flow-max")[0].rstrip())
        except Exception:
            return None
