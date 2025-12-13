
from Utils import calc_turn_by_given_degrees, calc_position_change, fmt_number
from enum import Enum

class Actions(Enum):
    MOVE  = 1
    TURN  = 2
    SET   = 3
    START = 4
    STOP  = 5


class Devices(Enum):
    WATER  = 1
    SOAP   = 2
    BRUSH  = 3


class RobotCleaner:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.device = Devices.WATER
        self.device_on = False


    def move(self, distance: float):
        dx, dy = calc_position_change(self.angle, distance)
        self.x += dx
        self.y += dy
        transfer_to_cleaner(f"POS {fmt_number(self.x)},{fmt_number(self.y)}")


    def turn(self, delta: float):
        self.angle = calc_turn_by_given_degrees(self.angle, delta)
        transfer_to_cleaner(f"ANGLE {round(self.angle, 2)}")


    def set_device(self, dev:Devices):
        self.device = dev
        transfer_to_cleaner(f"STATE {self.device.name}")


    def start(self):
        self.device_on = True
        transfer_to_cleaner(f"START WITH {self.device.name}")


    def stop(self):
        self.device_on = False
        transfer_to_cleaner("STOP")



def transfer_to_cleaner(message:str):
    print(message)

