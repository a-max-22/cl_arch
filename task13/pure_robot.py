import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка щётками

def move(dist,state):
    angle_rads = state.angle * (math.pi/180.0)   
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state)  
    return new_state

def turn(turn_angle,state):
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state)
    return new_state

def set_state(new_internal_state,state):
    if new_internal_state=='water':
        self_state = WATER  
    elif new_internal_state=='soap':
        self_state = SOAP
    elif new_internal_state=='brush':
        self_state = BRUSH
    else:
        return state  
    new_state = RobotState(
        state.x,
        state.y,
        state.angle,
        self_state)
    return new_state

def start(state):
    return state

def stop(state):
    return state
