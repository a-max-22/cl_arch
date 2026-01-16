import pure_robot

class ChainedOperation:
    def __init__(self, func = None, state = None):
        self.state = state
        self.func = ( lambda x:x ) if func is None else func
        self.operation = lambda x:x 

    def _execute(self, state):
        return self.operation(state)

    def __rshift__(self, op):
        self.state = op._execute(self.state)
        return self

    def __call__(self, *args):
        self.operation  = (lambda state: self.func(state, args))
        return self


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


def double_move(transfer,dist,state):
    return pure_robot.move(transfer,dist*2,state)


command_handlers_double_move = command_handlers.copy()
command_handlers_double_move['move'] = double_move


def transfer_to_cleaner(message):
    print (message)

def double_move(transfer,dist,state):
    return pure_robot.move(transfer,dist*2,state)

dispatcher = lambda transfer_func, cleaner_state, cmd_name, args: \
            dispatch_command(command_handlers, transfer_func, cleaner_state, cmd_name, args)

#dispatcher = lambda transfer_func, cleaner_state, cmd_name, args: \
#            dispatch_command(command_handlers_double_move, transfer_func, cleaner_state, cmd_name, args)


move       = ChainedOperation(lambda state, args : dispatcher(transfer_to_cleaner, state, 'move', args))
turn       = ChainedOperation(lambda state, args : dispatcher(transfer_to_cleaner, state, 'turn', args))
set_state  = ChainedOperation(lambda state, args : dispatcher(transfer_to_cleaner, state, 'set', args))
start      = ChainedOperation(lambda state, args : dispatcher(transfer_to_cleaner, state, 'start', args))
stop       = ChainedOperation(lambda state, args : dispatcher(transfer_to_cleaner, state, 'stop', args))
setup      = ChainedOperation(func = None, state=pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER))

