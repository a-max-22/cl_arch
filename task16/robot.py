
from collections import namedtuple
from dataclasses import dataclass
import math
from enum import Enum
from typing import List

Point = namedtuple("Point", "x y")    
Vector = namedtuple("Vector", "angle len")    
RobotState = namedtuple("RobotState", "point angle device")

class Device(Enum):
    WATER = 1  
    SOAP = 2   
    BRUSH = 3  


class Response:
    def __init__(self, status:bool):
        self.status = status


class Command: 
    def __init__(self, next):
        self.next_cmd = next
        self.response = Response(False)

    def next(self):
        return self.next_cmd 

    def interpret(self, state:RobotState):
        return state

    def get_response(self) -> Response: 
        return self.response

class InvalidCommand(Command):
    pass


def move_point(p:Point, v:Vector) -> Point:
    angle_rads = v.angle * (math.pi/180.0)
    x = p.x + v.len * math.cos(angle_rads)
    y = p.y + v.len * math.sin(angle_rads)
    return Point(x,y)


class MoveResponse(Response):
    def __init__(self, status:bool, distance:int):
        super().__init__(status)
        self.distance = distance
    
    def __str__(self):
        if self.status:
            return f'Moved successfully. Moved distance: {self.distance}'
        else: 
            return f'Move was unsuccessful.'
    

class MoveCommand(Command):
    def __init__(self, next:Command, distance:int):
        super().__init__(next)
        self.dist = distance

    def interpret(self, state:RobotState) -> RobotState:
        self.response = MoveResponse(True, self.dist)
        vec = Vector(state.angle, self.dist)
        new_point = move_point(state.point, vec)
        return RobotState(new_point, state.angle, state.device)


class TurnResponse(Response):
    def __init__(self, status:bool, angle:int):
        super().__init__(status)
        self.angle = angle
    
    def __str__(self):
        return f'Turned to : {self.angle}'
        
class TurnCommand(Command):
    def __init__(self, next:Command, angle:int):
        super().__init__(next)
        self.angle = angle

    def interpret(self, state:RobotState) -> RobotState:
        self.response = TurnResponse(True, self.angle)
        return RobotState(state.point, state.angle + self.angle, state.device)


class StateResponse(Response):
    def __init__(self, status:bool, device:Device):
        super().__init__(status)
        self.device = device
    
    def __str__(self):
        return f'new state to : {self.device.name}'
        
class StateCommand(Command):
    def __init__(self, next:Command, device:Device):
        super().__init__(next)
        self.device = device 

    def interpret(self, state:RobotState) -> RobotState:
        self.response = StateResponse(True, self.device)
        return RobotState(state.point, state.angle, self.device)


class StateResponse(Response):
    def __init__(self, status:bool, device:Device):
        super().__init__(status)
        self.device = device
    
    def __str__(self):
        return f'new state to : {self.device.name}'

class StartResponse(Response):
    def __str__(self):
        return 'Cleaning started'


class StartCommand(Command):
    def interpret(self, state:RobotState) -> RobotState:        
        self.response = StartResponse(True)
        return state

    def get_response(self) -> StartResponse: 
        return self.response


class StopResponse(Response):
    def __str__(self):
        return 'Cleaning stopped'


class StopCommand(Command):
    def interpret(self, state:RobotState) -> RobotState:        
        self.response = StopResponse(True)
        return state

    def get_response(self) -> StopResponse: 
        return self.response


class Interpreter:
    def __init__(self, commands:Command):
        self.head = commands
    
    def run(self, initial_state:RobotState) -> tuple[RobotState, List[str]]:
        node = self.head
        state = initial_state
        log = []
        while node is not None and not isinstance(node, StopCommand): 
            state = node.interpret(state)
            response = node.get_response()
            log.append(str(response))
            node = node.next()
        return state, log


@dataclass
class CommandToken:
    verb:str
    args:List[str]



invalid_command = InvalidCommand(None)

def parse_line(raw_line:str) -> List[str]:
    line = raw_line.upper().strip()
    if not line:
        return []
    line_parts = line.split()
    return line_parts

def tokenize_stream(commands_raw:List[str]) -> List[CommandToken]:
    tokens:List[CommandToken] = []
    
    for cmd_raw in commands_raw:
        cmd_parts = parse_line(cmd_raw)
        if len(cmd_parts) < 1:
            return []
        verb = cmd_parts[0]
        args = cmd_parts[1:]
        tokens.append(CommandToken(verb, args))
    return tokens

def is_int(string) -> bool:
    try:
        int(string)
        return True
    except:
        return False

def build_command(prev_command:Command, token:CommandToken):
    match token.verb:
        case 'MOVE' : return MoveCommand(prev_command, int(token.args[0])) \
                            if len(token.args) == 1 and is_int(token.args[0]) else invalid_command
        
        case 'TURN' : return TurnCommand(prev_command, int(token.args[0])) \
                            if len(token.args) == 1 and is_int(token.args[0]) else invalid_command

        case 'SET'  : return StateCommand(prev_command, Device[token.args[0]]) \
                            if len(token.args) == 1 and token.args[0] in Device.__members__.keys()\
                            else invalid_command
        
        case 'START': return StartCommand(prev_command) if len(token.args) == 0 else invalid_command

        case 'STOP' : return StopCommand(prev_command) if len(token.args) == 0 else invalid_command
        case _      : return invalid_command



def build_program(commands_raw:List[str]) -> Command:
    tokens = tokenize_stream(commands_raw)
    command = None

    for token in reversed(tokens):
        print(token) 
        built_command = build_command(command, token)
        if built_command != invalid_command:
            command = built_command
            continue
        print('inv com', token) 

    return command


def main():
    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop']
    program = build_program(commands)

    interpeter = Interpreter(program)
    state = RobotState(Point(0.0, 0.0), 0, Device.WATER)
    
    result_state, log = interpeter.run(state)
    print(result_state)
    
    for log_line in log: print(log_line)

main()