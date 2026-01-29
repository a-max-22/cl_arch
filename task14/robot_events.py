from abc import ABC, abstractmethod
from dataclasses import dataclass
import math

from robot import *


class Event(ABC):
    type:str = 'EVENT'

    @abstractmethod
    def apply(self, state: RobotState) -> RobotState:
        pass
    
    def get_event_type(self) -> str:
        return self.type


@dataclass
class RobotMoveRequested(Event):
    distance: float
    type: str = 'ROBOT_MOVE_REQUESTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type} {self.distance}'


@dataclass
class RobotMovedEvent(Event):
    distance: float
    type: str = 'ROBOT_MOVED'
    
    def apply(self, state: RobotState) -> RobotState:
        angle_rads = state.angle * (math.pi/180.0)
        return RobotState(
            x=state.x + self.distance * math.cos(angle_rads),
            y=state.y + self.distance * math.sin(angle_rads),
            angle=state.angle,
            state=state.state
        )
    
    def __str__(self) -> str:
        return f'{self.type} {self.distance}'


@dataclass
class RobotTurnRequestedEvent(Event):
    angle: float
    type: str = 'ROBOT_TURN_REQUESTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type} {self.angle}'


@dataclass
class RobotTurnedEvent(Event):
    angle: float
    type: str = 'ROBOT_TURNED'

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle + self.angle,
            state=state.state
        )
    
    def __str__(self) -> str:
        return f'{self.type} {self.angle}'


@dataclass
class RobotStateChangeRequestedEvent(Event):
    new_state: float
    type: str = 'ROBOT_STATE_CHANGE_REQUESTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type} {self.new_state}'


@dataclass
class RobotStateChangedEvent(Event):
    new_state: CleaningMode
    type: str = 'ROBOT_STATE_CHANGED'
    
    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=self.new_state.value
        )
    
    def __str__(self) -> str:
        return f'{self.type} {self.new_state}'


@dataclass
class RobotStartRequestedEvent(Event):
    type: str = 'ROBOT_START_REQUESTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type}'

@dataclass
class RobotStartedEvent(Event):
    type: str = 'ROBOT_STARTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type}'

@dataclass
class RobotStopRequestedEvent(Event):
    type: str = 'ROBOT_STOP_REQUESTED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type}'

@dataclass
class RobotStoppedEvent(Event):
    type: str = 'ROBOT_STROBOT_STOPPED'

    def apply(self, state: RobotState) -> RobotState:
        return state
    
    def __str__(self) -> str:
        return f'{self.type}'
