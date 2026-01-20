import pure_robot



class RobotCommand:
    def __init__(self, func:callable, *args):
        self.func = func
        self.args = args

    def execute(self, state):
        return self.func(state, self.args)

class Setup(RobotCommand):
    def __init__(self):
        super().__init__(setup, [])


def setup(state, args):
    return pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

def transfer_to_cleaner(message):
    print(message)

command_handlers = {
    'move' :pure_robot.move,
    'turn' :pure_robot.turn,
    'set'  :pure_robot.set_state,
    'start':pure_robot.start,
    'stop' :pure_robot.stop,
    'null' :lambda x: x
}

def dispatch_command(command_handlers, transfer_func, cleaner_state, cmd_name, args):
    return command_handlers[cmd_name](transfer_func, *args, cleaner_state)


dispatcher = lambda transfer_func, cleaner_state, cmd_name, args: \
            dispatch_command(command_handlers, transfer_func, cleaner_state, cmd_name, args)


move       = lambda state, args : dispatcher(transfer_to_cleaner, state, 'move', args)
turn       = lambda state, args : dispatcher(transfer_to_cleaner, state, 'turn', args)
set_state  = lambda state, args : dispatcher(transfer_to_cleaner, state, 'set', args)
start      = lambda state, args : dispatcher(transfer_to_cleaner, state, 'start', args)
stop       = lambda state, args : dispatcher(transfer_to_cleaner, state, 'stop', args)