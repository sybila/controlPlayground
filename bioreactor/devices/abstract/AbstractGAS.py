from .device import Device

# Abstract Gas Analyser
class AbstractGAS(Device):
    def __init__(self, particle, ID, adress):
        super(AbstractGAS, self).__init__(particle, ID, adress)

    def get_co2_air(self):
        '''
        Returns CO2 in air.
        '''
        raise NotImplementedError("The method not implemented")

    def get_small_valves(self):
        '''
        Obtain settings of individual vents of GAS device.

        Represented as one byte, where first 6 bits represent 
        vents indexed as in a picture scheme available here: 
        https://i.imgur.com/jSeFFaO.jpg

        Returns:
            string: byte representation of vents settings.
        '''
        raise NotImplementedError("The method not implemented")

    def set_small_valves(self, mode):
        '''
        Changes settings of individual vents of GAS device.

        Can be set by one byte (converted to int), where first 6
        bits represent vents indexed as in a picture scheme
        available here: https://i.imgur.com/jSeFFaO.jpg

        Mode 0 - normal mode, output from GMS goes to PBR (255)
        Mode 1 - reset mode, N2 (nitrogen) goes to PBR (239)
        Mode 2 - no gas input to PBR (249)
        Mode 3 - output of PBR goes to input of PBR (246)

        Args:
            mode (int): chosen mode (0 to 3)
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

    def get_flow(self):
        '''
        Actual flow being send from GAS to the PBR.

        Returns:
            float: The current flow in L/min.
        '''
        raise NotImplementedError("The method not implemented")

    def get_flow_target(self):
        '''
        Actual desired flow.

        Returns:
            float: The desired flow in L/min.
        '''
        raise NotImplementedError("The method not implemented")

    def set_flow_target(self, flow):
        '''
        Set flow we want to achieve.

        Args:
            flow (float): flow in L/min we want to achieve (max given by get_flow_max)
        Returns:
            bool: True if was succesful, False otherwise.
        '''
        raise NotImplementedError("The method not implemented")

    def get_flow_max(self):
        '''
        Maximal allowed flow.

        Returns:
            float: The maximal flow in L/min
        '''
        raise NotImplementedError("The method not implemented")
