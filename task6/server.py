import pure_robot


class CommandResult:
    def __init__(self, initial_value:pure_robot.RobotState):
        self.result = initial_value

    def get_x(self):
        return self.result.x

    def get_y(self):
        return self.result.y

    def get_angle(self):
        return self.result.angle

    def get_state(self):
        return self.result.state

    

# класс Чистильщик API
class CleanerApi:

    # конструктор 
    def __init__(self):
        pass

    # взаимодействие с роботом вынесено в отдельную функцию
    def transfer_to_cleaner(self, message):
        print (message)


    def execute_command(self, cmd, previous_result: CommandResult = None) -> CommandResult:
        if previous_result is None: 
            previous_result = CommandResult(pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER))

        if cmd[0]=='move':
            return pure_robot.move(self.transfer_to_cleaner,int(cmd[1]), previous_result.get_state()) 
        elif cmd[0]=='turn':
            return pure_robot.turn(self.transfer_to_cleaner, int(cmd[1]), previous_result.get_state())
        elif cmd[0]=='set':
            return pure_robot.set_state(self.transfer_to_cleaner, cmd[1], previous_result.get_state()) 
        elif cmd[0]=='start':
            return pure_robot.start(self.transfer_to_cleaner, previous_result.get_state())
        elif cmd[0]=='stop':
            return pure_robot.stop(self.transfer_to_cleaner, previous_result.get_state())

        return previous_result


    def activate_cleaner(self,code):
        for command in code:
            cmd = command.split(' ')
            command_result = self.execute_command(cmd)
