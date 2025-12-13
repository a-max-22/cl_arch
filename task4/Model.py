

from RobotCleaner import RobotCleaner, Devices, Actions

ActionsNames = {
    "MOVE" :Actions.MOVE,
    "TURN" :Actions.TURN,
    "SET"  :Actions.SET,
    "START":Actions.START,
    "STOP" :Actions.STOP
}


DevicesNames = {
    "WATER" :Devices.WATER,
    "SOAP"  :Devices.SOAP,
    "BRUSH" :Devices.BRUSH
}


def name_to_value(names_to_values:dict, value:str):
    if value in names_to_values:
        return names_to_values[value]
    
    return None


def get_device_by_name(device_name:str):
    return name_to_value(DevicesNames, device_name)

def get_action_by_name(action_name:str):
    return name_to_value(ActionsNames, action_name)

