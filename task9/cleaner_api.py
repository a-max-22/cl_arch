import pure_robot


def transfer_to_cleaner(message):
    print (message)


def calc_new_state(command_func:callable, args, state):
    return command_func(transfer_to_cleaner, *args, state)

command_handlers = {
    'move' :pure_robot.move,
    'turn' :pure_robot.turn,
    'set'  :pure_robot.set_state,
    'start':pure_robot.start,
    'stop' :pure_robot.stop
}

def dispatch_command(command_handlers, transfer_func, cleaner_state, cmd_name, args):
    return command_handlers[cmd_name](transfer_func, *args, cleaner_state)


def double_move(transfer,dist,state):
    return pure_robot.move(transfer,dist*2,state)


command_handlers_double_move = command_handlers.copy()
command_handlers_double_move['move'] = double_move



class RobotApi:

    def setup(self, f_transfer, f_dispatcher):
        self.f_dispatcher = f_dispatcher
        self.f_transfer = f_transfer

    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        cmd = command.split(' ')
        if cmd[0]=='move':
             args = [int(cmd[1])]
             self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state,'move', args)
        elif cmd[0]=='turn':
             args = [int(cmd[1])]
             self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state,'turn', args)
        elif cmd[0]=='set':
             args = [cmd[1]]
             self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state,'set', args)
        elif cmd[0]=='start':
             args = []
             self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state,'start', args)
        elif cmd[0]=='stop':
             args = []
             self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state,'stop', args)
        return self.cleaner_state

    def __call__(self, command):
        return self.make(command)

def transfer_to_cleaner(message):
    print (message)

def double_move(transfer,dist,state):
    return pure_robot.move(transfer,dist*2,state)

api = RobotApi()

dispatcher = lambda transfer_func, cleaner_state, cmd_name, args: \
            dispatch_command(command_handlers, transfer_func, cleaner_state, cmd_name, args)

#dispatcher = lambda transfer_func, cleaner_state, cmd_name, args: \
#            dispatch_command(command_handlers_double_move, transfer_func, cleaner_state, cmd_name, args)

api.setup(transfer_to_cleaner, dispatcher)
