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
    'stop' :pure_robot.stop,
    'null' :lambda x: x
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
    
    def cmd_get_args(self, cmd_name, raw_args):
        if cmd_name=='move':
             cmd_name, args = ('null',[]) if len(raw_args) != 1 else cmd_name, [int(raw_args[0])]
        elif cmd_name=='turn':
             cmd_name, args = ('null',[])  if len(raw_args) != 1 else cmd_name, [int(raw_args[0])]
        elif cmd_name=='set':
             cmd_name, args = ('null',[])  if len(raw_args) != 1 else cmd_name, [raw_args[0]]
        elif cmd_name=='start':
             cmd_name, args = ('null',[])  if len(raw_args) != 0 else cmd_name, []
        elif cmd_name=='stop':
             cmd_name, args = ('null',[])  if len(raw_args) != 0 else cmd_name, []
        else:
             cmd_name, args = ('null',[])  
        return cmd_name, args       


    def process_command(self, cmd_name, raw_args):
        cmd_verb, args = self.cmd_get_args(cmd_name, raw_args)
        self.cleaner_state = self.f_dispatcher(self.f_transfer, self.cleaner_state, cmd_verb, args)
        
        return self.cleaner_state
    
    def process_stream(self, cmd_stream):
        raw_args = []
        for item in cmd_stream: 
            if item not in command_handlers:
                raw_args.append(item)
                continue
    
            cmd_name = item
            self.process_command(cmd_name, raw_args)
            raw_args = []
            continue

    def make(self, command_stream_raw):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        
        cmd_stream = command_stream_raw.split(' ')
        self.process_stream(cmd_stream)

    def __call__(self, command_stream):
        return self.make(command_stream) 

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
