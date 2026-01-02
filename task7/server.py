
import pure_robot
from abc import ABC, abstractmethod

class CleanerApiInterface(ABC):
    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def activate(self, command):
        pass


class CommandParser:
    def __init__(self):
        pass

    def parse_command(self, cmd_code):
        cmd = cmd_code.split(' ')
        if cmd[0]=='move':
            return 'move', []
        elif cmd[0]=='turn':
            return 'turn', []
        elif cmd[0]=='set':
            return 'set', []
        elif cmd[0]=='start':
            return 'start', []
        elif cmd[0]=='stop':
            return 'stop', []


# класс Чистильщик API
class CleanerApi(CleanerApiInterface):
    def __init__(self):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        self.parser = CommandParser()

    def transfer_to_cleaner(self,message):
        print (message)

    def get_state(self):
        return self.cleaner_state.state

    def activate(self,code):
        for command in code:
            cmd_name, args = self.parser.parse_command(command)
            if cmd_name =='move':
                self.cleaner_state = pure_robot.move(self.transfer_to_cleaner,
                    args[1],self.cleaner_state) 
            elif cmd_name =='turn':
                self.cleaner_state = pure_robot.turn(self.transfer_to_cleaner,
                    args[1],self.cleaner_state)
            elif cmd_name=='set':
                self.cleaner_state = pure_robot.set_state(self.transfer_to_cleaner,
                    args[1],self.cleaner_state) 
            elif cmd_name =='start':
                self.cleaner_state = pure_robot.start(self.transfer_to_cleaner,
                    self.cleaner_state)
            elif cmd_name =='stop':
                self.cleaner_state = pure_robot.stop(self.transfer_to_cleaner,
                    self.cleaner_state)



