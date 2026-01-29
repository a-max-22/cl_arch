from enum import Enum
from dataclasses import dataclass

@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int

class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3