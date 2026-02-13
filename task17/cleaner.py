import math
from typing import Self
from enum import Enum

def transfer_to_cleaner(message):
    print(message)


class Cleaner:

    WATER = 1 
    SOAP  = 2 
    BRUSH = 3 

    TURN_NIL = 0
    TURN_OK = 1

    MOVE_NIL = 0
    MOVE_OK = 1
    MOVE_ERR = 2

    SET_NIL = 0
    SET_OK = 1
    SET_ERR = 2


    def __init__(self, transfer:callable, x:float, y:float, angle:int, state:int):
        self.x = x
        self.y = y
        self.angle = angle
        self.state = state
        self.transfer = transfer
       
        self.turn_status = self.TURN_NIL
        self.move_status = self.MOVE_NIL
        self.set_status = self.SET_NIL


    def move(self, dist) -> Self:
        angle_rads = self.angle * (math.pi/180.0)
        x_new = self.x + dist * math.cos(angle_rads)
        y_new = self.y + dist * math.sin(angle_rads)

        # можно добавить дополнительную проверку позиции
        self.move_status = self.MOVE_OK        
        self.transfer(('POS(',self.x,',',self.y,')'))
        
        return Cleaner(self.transfer, x_new, y_new, self.angle, self.state) 

    def turn(self,turn_angle) -> Self:
        angle_new = self.angle + turn_angle

        self.turn_status = self.TURN_OK        
        self.transfer(('ANGLE',self.angle))

        return Cleaner(self.transfer, self.x, self.y, angle_new, self.state) 


    def set_state(self, new_state) -> Self:
        if new_state=='water':
            self.state = self.WATER  
        elif new_state=='soap':
            self.state = self.SOAP
        elif new_state=='brush':
            self.state = self.BRUSH
        else: 
            self.set_status = self.SET_ERR
            return self
        
        self.set_status = self.SET_OK
        self.transfer(('STATE', self.state))
        return Cleaner(self.transfer, self.x, self.y, self.angle, self.state) 

    def start(self) -> Self:
        self.transfer(('START WITH',self.state))
        return self

    def stop(self) -> Self:
        self.transfer(('STOP',))
        return self
    
    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def get_device(self) -> tuple[float, float]:
        if self.state == self.WATER:
            return 'water'  
        elif self.state == self.SOAP:
            return 'soap'
        elif self.state == self.BRUSH:
            return 'brush'

    def get_direction(self) -> int:
        return self.angle

    def is_move_ok(self):
        return self.move_status == self.MOVE_OK
    
    def is_turn_ok(self):
        return self.turn_status == self.TURN_OK

    def is_set_state_ok(self):
        return self.set_status == self.SET_OK



def init_cleaner(transfer_func) -> Cleaner:
    return Cleaner(transfer_func, 0.0, 0.0, 0, Cleaner.WATER)


def make(cleaner:Cleaner, code:list[str]) -> Cleaner:
    for command in code:
        cmd = command.split(' ')
        if cmd[0]=='move':
            cleaner_new = cleaner.move(int(cmd[1]))
            cleaner = (cleaner_new if cleaner.is_move_ok() else cleaner)
        
        elif cmd[0]=='turn':
            cleaner_new = cleaner.turn(int(cmd[1]))         
            cleaner = (cleaner_new if cleaner.is_turn_ok() else cleaner)

        elif cmd[0]=='set':
            cleaner_new = cleaner.set_state(cmd[1]) 
            cleaner = (cleaner_new if cleaner.is_set_state_ok() else cleaner)

        elif cmd[0]=='start':
            cleaner = cleaner.start()

        elif cmd[0]=='stop':
            cleaner = cleaner.stop()
            
    return cleaner