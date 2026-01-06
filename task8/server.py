
import pure_robot


def transfer_to_cleaner(message):
    print (message)


def calc_new_state(command_func:callable, args, state):
    return command_func(transfer_to_cleaner, *args, state)


class CleanerApi:

    def __init__(self):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def get_x(self):
        return self.cleaner_state.x

    def get_y(self):
        return self.cleaner_state.y

    def get_angle(self):
        return self.cleaner_state.angle

    def get_state(self):
        return self.cleaner_state.state

    def activate_cleaner(self,code):
        for command in code:
            cmd = command.split(' ')
            cmd_name = cmd[0] 

            match cmd_name: 
                case 'move':
                    args = [int(cmd[1])]
                    self.cleaner_state = calc_new_state(pure_robot.move, 
                                         args, self.cleaner_state) 
                case 'turn':
                    args = [int(cmd[1])]
                    self.cleaner_state = calc_new_state(pure_robot.turn, 
                                        args, self.cleaner_state) 

                case 'set':
                    args = [cmd[1]]
                    self.cleaner_state = calc_new_state(pure_robot.set_state, args, self.cleaner_state) 

                case 'start':
                    args = []
                    self.cleaner_state = calc_new_state(pure_robot.start, args, self.cleaner_state) 

                case 'stop':
                    args = []
                    self.cleaner_state = calc_new_state(pure_robot.stop, args, self.cleaner_state)