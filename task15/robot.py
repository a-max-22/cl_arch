from functools import wraps
from collections import namedtuple
import math

RobotState = namedtuple("RobotState", "x y angle state")
Resources =  namedtuple("Resources", "water soap")

RobotStateExtended = namedtuple("RobotStateExtended", \
                                "x y angle state resources washing")


WATER = 1  
SOAP = 2   
BRUSH = 3  

class StateMonad:
    def __init__(self, state, log=None):
        self.state = state
        self.log = log or []
    
    def bind(self, func):
        new_state, new_log = func(self.state, self.log)
        return StateMonad(new_state, new_log)



def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))
    
    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)

def move_bounds_decorator(move_func):
    def inner(dist, old_state, log):
        moved_state, log_new = move_func(dist)(old_state, log)

        x,y, status = check_position(moved_state.x, moved_state.y)
        if status == MoveResponse.OK:
            return moved_state, log_new
        
        new_state = RobotStateExtended(
            x,
            y,
            moved_state.angle,
            moved_state.state,
            moved_state.resources,
            moved_state.washing
        )
        return new_state, log + \
            [f'HIT BARRIER ({int(new_state.x)},{int(new_state.y)})']
    
    @wraps(move_func)
    def wrap(dist):
        return lambda x,y: inner(dist, x, y)
    
    return wrap

def resources_use_decorator(move_func):
    def inner(dist, old_state, log):
        moved_state, log_new = move_func(dist)(old_state, log)
        if not moved_state.washing:
            return moved_state, log_new
        
        total_distance = abs(moved_state.x - old_state.x) + \
                         abs(moved_state.y - old_state.y)
        
        resources_consumption_rate = 1
        resources_consumed = total_distance * resources_consumption_rate

        if moved_state.state == WATER:
            water_left =  max(0, moved_state.resources.water - resources_consumed)
            soap_left =  moved_state.resources.soap
            log_entry = [f'LEFT {water_left} WATER']
        elif moved_state.state == SOAP:
            water_left = moved_state.resources.water
            soap_left =  max(0, moved_state.resources.soap - resources_consumed)
            log_entry = [f'LEFT {soap_left} SOAP']
        else:
            water_left = moved_state.resources.water
            soap_left = moved_state.resources.soap
            device_name = 'BRUSH'
            log_entry = []
        
        new_state = RobotStateExtended(
                moved_state.x,
                moved_state.y,
                moved_state.angle,
                moved_state.state,
                Resources(water_left, soap_left),
                moved_state.washing
            )
        print('consumed ', \
              resources_consumed,\
              moved_state.resources.soap - resources_consumed, 
              max(0, moved_state.resources.soap - resources_consumed))
        return new_state, log + log_entry
    
    @wraps(move_func)
    def wrap(dist):
        return lambda x,y: inner(dist, x, y)
    
    return wrap


def check_resources(resources, new_mode: int) -> SetStateResponse:
    if new_mode == WATER and resources.water <= 0:
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP and resources.soap <= 0:
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK


def resources_check_decorator(func):
    def inner(old_state, log):
        new_state, log_new = func()(old_state, log)
        chec_status = check_resources(new_state.resources, new_state.state)
        if chec_status == SetStateResponse.OK:
            return new_state, log_new 
        log_entry = []
        if new_state.state == WATER:
            log_entry = ['NOT ENOUGH WATER']
        elif new_state.state == SOAP:
            log_entry = ['NOT ENOUGH SOAP']

        return old_state, log + log_entry

    
    @wraps(func)
    def wrap():
        return lambda x,y: inner(x, y)
    
    return wrap


@move_bounds_decorator
@resources_use_decorator
def move(dist):
    def inner(old_state, log):
        angle_rads = old_state.angle * (math.pi/180.0)
        new_state = RobotStateExtended(
            old_state.x + dist * math.cos(angle_rads),
            old_state.y + dist * math.sin(angle_rads),
            old_state.angle,
            old_state.state,
            old_state.resources,
            old_state.washing
        )
        return new_state, log + [f'POS({int(new_state.x)},{int(new_state.y)})']
    return inner

def turn(angle):
    def inner(old_state, log):
        new_state = RobotStateExtended(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state,
            old_state.resources,
            old_state.washing
        )
        return new_state, log + [f'ANGLE {new_state.angle}']
    return inner


def set_state(new_mode):
    def inner(old_state, log):
        new_state = RobotStateExtended(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode, 
            old_state.resources,
            old_state.washing
        )
        return new_state, log + [f'STATE {new_mode}']
    return inner


@resources_check_decorator
def start():
    def inner(old_state, log):
        new_state = RobotStateExtended(
            old_state.x,
            old_state.y,
            old_state.angle,
            old_state.state, 
            old_state.resources,
            True
        )
        return new_state, log + ['START']

    return inner

def stop():
    def inner(old_state, log):
        new_state = RobotStateExtended(
            old_state.x,
            old_state.y,
            old_state.angle,
            old_state.state, 
            old_state.resources,
            True
        )
        return new_state, log + ['STOP']

    return inner


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"


class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


initial_state = StateMonad(RobotStateExtended(0.0, 0.0, 0, WATER,\
                                               Resources(10, 20),
                                               False))

result = (initial_state
    .bind(move(200))
    .bind(turn(-90))
    .bind(set_state(SOAP))
    .bind(start())
    .bind(move(-50))
    .bind(stop())
    .bind(start())
    .bind(move(30))
    .bind(stop()))


print(f"Final state: {result.state}")
print(f"Log: {result.log}")