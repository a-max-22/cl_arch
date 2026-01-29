
from dataclasses import dataclass
from robot_events import *

from typing import List, Protocol
from robot import *


class Command(Protocol):
    def handle(self) -> List[Event]:
        pass
    
    def get_command_type(self) -> str:
        pass

@dataclass
class MoveCommand:
    distance: float
    
    def handle(self) -> List[Event]:
        return [RobotMoveRequested(self.distance)]
    
    def get_command_type(self) -> str:
        return f'MOVE {self.distance}'

@dataclass
class TurnCommand:
    angle: float
    
    def handle(self) -> List[Event]:
        return [RobotTurnRequestedEvent(self.angle)]
    
    def get_command_type(self) -> str:
        return f'TURN {self.angle}'

@dataclass
class SetStateCommand:
    new_state: CleaningMode
    
    def handle(self) -> List[Event]:
        return [RobotStateChangeRequestedEvent(self.new_state)]
    
    def get_command_type(self) -> str:
        return f'SET_STATE {self.new_state.name}'

@dataclass
class StartCommand:
    def handle(self) -> List[Event]:
        return [RobotStartRequestedEvent()]
    
    def get_command_type(self) -> str:
        return 'START'

@dataclass
class StopCommand:
    def handle(self) -> List[Event]:
        return [RobotStopRequestedEvent()]
    
    def get_command_type(self) -> str:
        return 'STOP'