import os, sys

workspace = os.path.dirname(__file__)

sys.path.append(os.path.join(workspace, 'devices/'))
import particle

GAS_TYPES = ["CO2", "Air", "N2"]

# --------------------------------------------------------------
# API

node = particle.Particle('root', '/root/control/', '192.168.17.13')
node.add_device("PBR", "PBR07", 72700007)
node.add_device("GMS", "GMS", 46700003)
node.add_device("GAS", "GAS", 42700007)

# PBR = Bioreactor.PBR()
# GMS = GasMixer.GMS()
# GAS = GasAnalyser.GAS()

# Temperature (Bioreactor)

def get_temp_settings():
    '''
    Get information about currently set temperature, maximal and
    minimal allowed temperature.

    Returns:
        dict: The current settings structured in a dictionary.
    '''
    results = ["set", "min", "max"]
    try:
        values = execute(PBR, "get-thermoregulator-settings")[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, list(map(float, values[1:-1]))))

def get_temp():
    '''
    Get current temperature in Celsius degree.

    Returns:
        float: The current temperature.
    '''
    try:
        return float(execute(PBR, "get-current-temperature")[0])
    except Exception:
        return None

def set_temp(temp):
    '''
    Set desired temperature in Celsius degree.

    Args:
        temp (float): The temperature.
    Returns:
        bool: True if was succesful, False otherwise.
    '''
    try:
        return execute(PBR, "set-thermoregulator-temp", [temp])[0].rstrip() == 'ok'
    except Exception:
        return False

# pH (Bioreactor)

def get_ph():
    '''
    Get current pH.

    Returns:
        float: The current pH.
    '''
    try:
        return float(execute(PBR, "get-ph", [5, 0])[0])
    except Exception:
        return None

# valve (Gas Mixer)

def get_valve_flow(valve):
    '''
    Get value (L/min) of current flow in the given valve.

    Args:
        valve (int): ID of the valve (0 for CO2, 1 for Air)
    Returns:
        dict: The current settings of the valve flow and actual value, both in (L/min).
    '''
    results = ["current", "set"]
    try:
        values = execute(GMS, "get-valve-flow", [valve])[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, list(map(float, values[1:-1]))))
    '''
    Set flow to value for the given valve.
    '''
def set_valve_flow(valve, value):
    '''
    Set value (L/min) of current flow in the given valve.

    Args:
        valve (int): ID of the valve (0 for CO2, 1 for Air)
        value (float): desired value for valve flow in (L/min).
    Returns:
        bool: True if was succesful, False otherwise.
    '''
    try:
        return execute(GMS, "set-valve-tflow", [valve, value])[0].rstrip() == 'ok'
    except Exception:
        return None

def get_valve_info(valve):
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
        values = execute(GMS, "get-valve-info", [valve])[0].rstrip()[1:-1].split()
    except Exception:
        return None
    return dict(zip(results, [float(values[1]), GAS_TYPES[int(values[3])]]))


# ----------------------------
# new added, docstrings needed

# (Gas Analyser)

def get_co2_air():
    '''
    TBA
    '''
    try:
        return float(execute(GAS, "get-co2-air")[0].rstrip())
    except Exception:
        return None

def get_small_valves():
    '''
    Obtain settings of individual vents of GAS device.

    Represented as one byte, where first 6 bits represent 
    vents indexed as in a picture scheme available here: 
    https://i.imgur.com/jSeFFaO.jpg

    Returns:
        string: byte representation of vents settings.
    '''
    try:
        value = int(execute(GAS, "get-small-valves")[0].rstrip())
    except Exception:
        return None
    return bin(value)[2:]

def set_small_valves(mode):
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
    modes = {0 : "11111011", 1 : "11110011"}
    try:
        return execute(GAS, "set-small-valves", [int(modes[mode], 2)])[0].rstrip() == 'ok'
    except Exception:
        return None

def get_flow():
    '''
    Actual flow being send from GAS to the PBR.

    Returns:
        float: The current flow in L/min.
    '''
    try:
        return float(execute(GAS, "get-flow", [1])[0].rstrip())
    except Exception:
        return None

def get_flow_target():
    '''
    Actual desired flow.

    Returns:
        float: The desired flow in L/min.
    '''
    try:
        return float(execute(GAS, "get-flow-target")[0].rstrip())
    except Exception:
        return None

def set_flow_target(flow):
    '''
    Set flow we want to achieve.

    Args:
        flow (float): flow in L/min we want to achieve (max given by get_flow_max)
    Returns:
        bool: True if was succesful, False otherwise.
    '''
    try:
        return execute(GAS, "get-flow-target", [flow])[0].rstrip() == 'ok'
    except Exception:
        return None

def get_flow_max():
    '''
    Maximal allowed flow.

    Returns:
        float: The maximal flow in L/min
    '''
    try:
        return float(execute(GAS, "get-flow-max")[0].rstrip())
    except Exception:
        return None
