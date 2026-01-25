from dataclasses import dataclass
from typing import List, Protocol, Any, Callable
from enum import Enum
import math
import pure_robot  


# Состояние робота
@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int

# Режимы работы
class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


# Протокол для команд
class Command(Protocol):
    def execute(self) -> RobotState:
        pass
    
    def log(self) -> str:
        pass

@dataclass
class Event:
    action:Callable[RobotState, tuple]
    params:tuple

# Конкретные команды
@dataclass
class MoveCommand:
    distance: float
    
    def execute(self) -> Event:
        return Event(pure_robot.move, [self.distance])
    
    def log(self) -> str:
        return f'MOVE {self.distance}'

@dataclass
class TurnCommand:
    angle: float
    
    def execute(self) -> RobotState:
        return Event(pure_robot.turn, [self.angle])
    
    def log(self) -> str:
        return f'TURN {self.angle}'

@dataclass
class SetStateCommand:
    new_state: CleaningMode
    
    def execute(self) -> RobotState:
        return Event(pure_robot.set_state, [self.new_state])
    
    def log(self) -> str:
        return f'SET_STATE {self.new_state.name}'

@dataclass
class StartCommand:
    def execute(self) -> RobotState:
        return Event(pure_robot.start, [])

    def log(self) -> str:
        return 'START'

@dataclass
class StopCommand:
    def execute(self) -> RobotState:
        return Event(pure_robot.stop, [])
    
    def log(self) -> str:
        return 'STOP'



class EventStore:
    def __init__(self, initial_state:RobotState):
        self.events: List[Command] = []
        self.state = initial_state

    def add(self, event:Event):
        self.events.append(event)
    
    def get_result_state(self):
        result_state = self.state 
        for event in self.events:
            result_state = event.action(*event.params, result_state)
        return result_state


class CommandHandler:
    def __init__(self):
        self.event_store = EventStore(pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER))
        self.logs = []
        
    def exec_command(self, command: Command):
        self.event_store.add(command.execute())
        self.logs.append(command.log())
        
    def get_state(self) -> tuple[RobotState, List[str]]:
        current_state = self.event_store.get_result_state()        
        return current_state, self.logs

