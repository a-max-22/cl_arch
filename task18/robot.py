from enum import Enum
from collections import namedtuple
import math
from typing import Tuple, List, Optional, Self, Set

class MoveResponse(Enum):
    OK = 1
    BARRIER = 2

class SetStateResponse(Enum):
    OK = 1
    NO_WATER = 2
    NO_SOAP  = 3

class OperationResponse(Enum):
    OP_POSSIBLE  = 1
    OP_FORBIDDEN = 2


class Device(Enum):
    WATER = 1  
    SOAP = 2   
    BRUSH = 3  


RobotState = namedtuple("RobotState", "x y angle state")


class Operation:
    def __init__(self):
        pass
    
    def __hash__(self):
        return hash(type(self).__name__)
    
    def __call__(self, state: RobotState, log: List[str], possible_ops:Set[Self]) -> \
        tuple[RobotState, List[str], OperationResponse]:
        if type(self) not in possible_ops:
            return state, log + ['OPERATION FORBIDDEN'], OperationResponse.OP_POSSIBLE
        return self._do_operation(state, log)
    
    def _do_operation(self, state:RobotState, log:List[str]) -> \
        tuple[RobotState, List[str], OperationResponse]:
        return state, log


class StateMonad:
    def __init__(self, state: RobotState, log: List[str] = None, possible_operations:Set[Operation] = set()):
        self.state = state
        self.log = log or []
        if possible_operations == set():
            self.possible_operations = get_all_possible_operations()
        else:
            self.possible_operations = possible_operations
    
    def bind(self, func:Operation) -> Self:
        new_state, new_log, result = func(self.state, self.log, self.possible_operations)
        possible_operations = get_possible_operations_by_state(new_state, func, result)
        return StateMonad(new_state, new_log, possible_operations)


def get_possible_operations_by_state(state:RobotState, op:Operation, op_result):
    if isinstance(op, Move) and op_result == MoveResponse.BARRIER:
        return set([Turn, SetState])
    return get_all_possible_operations() 

def get_all_possible_operations():
    return set([Move, Turn, SetState])

def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))
    
    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)


class Move(Operation):
    def __init__(self, dist:int = 0):
        self.dist:int = dist
    
    def _do_operation(self, state: RobotState, log: List[str]) -> \
        tuple[RobotState, List[str], OperationResponse]:
        angle_rads = state.angle * (math.pi/180.0)
        new_x = state.x + self.dist * math.cos(angle_rads)
        new_y = state.y + self.dist * math.sin(angle_rads)
    
        constrained_x, constrained_y, move_result = check_position(new_x, new_y)
        
        new_state = RobotState(
            constrained_x,
            constrained_y,
            state.angle,
            state.state
        )
    
        message = (f'POS({int(constrained_x)},{int(constrained_y)})' 
                if move_result == MoveResponse.OK 
                else f'HIT_BARRIER at ({int(constrained_x)},{int(constrained_y)})')
        
        return new_state, log + [message], move_result


class Turn(Operation):
    def __init__(self, angle:int = 0):
        self.angle:int = angle

    def _do_operation(self, state: RobotState, log: List[str]) -> \
            tuple[RobotState, List[str], OperationResponse]:
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self.angle,
            state.state
        )
        return new_state, log + [f'ANGLE {new_state.angle}'], MoveResponse.OK


def check_resources(new_mode):
    return SetStateResponse.OK


class SetState(Operation):
    def __init__(self, new_device:Device = Device.WATER):
        self.device:Device = new_device

    def _do_operation(self, state: RobotState, log: List[str]) -> \
            tuple[RobotState, List[str], OperationResponse]:
        resource_check = check_resources(self.device)
        
        if resource_check != SetStateResponse.OK:
            message = f'RESOURCE ERROR: {resource_check} for mode {self.device.name}'
            return state, log + [message], resource_check
        
        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self.device
        )
        return new_state, log + [f'STATE {self.device.name}'], SetStateResponse.OK




initial_state = StateMonad(RobotState(0.0, 0.0, 0, Device.WATER))
result = (initial_state
    .bind(Move(150))
    .bind(Move(50))
    .bind(SetState(Device.SOAP))
    .bind(Turn(-90))
    .bind(Move(50)))

print(f"Final state: {result.state}")
print(f"Log: {result.log}")


