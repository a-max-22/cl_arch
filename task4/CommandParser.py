from RobotCleaner import RobotCleaner, Actions
from Model import get_device_by_name, get_action_by_name
from Utils import log

class CommandsParser:
    PARSE_OK  = 0
    PARSE_ERR = 1

    def __init__(self):
        self.parsed_command_name  = ''
        self.parsed_command_args  = ''


        self.arg_parsers = {
            Actions.MOVE  : lambda args:check_first_arg_conv_to_float(args),
            Actions.TURN  : lambda args:check_first_arg_conv_to_float(args),
            Actions.SET   : lambda args:check_if_the_only_arg_and_convert(get_device_by_name, args),
            Actions.START : lambda args:check_no_args(args), 
            Actions.STOP  : lambda args:check_no_args(args)
            }


    def parse_command(self, raw_line:str): 
        action_name, raw_args = get_tokens_from_raw_line(raw_line)
        if action_name is None:
            return self.PARSE_ERR
        
        action = get_action_by_name(normalize_str(action_name))
        if action is None: 
            log('Incorrect action name %s provided' % action_name)
            return self.PARSE_ERR
        try:
            args = parse_command_args(action, raw_args, self.arg_parsers)
        except ValueError as e:
            log(e)
            return self.PARSE_ERR
        
        self.parsed_action_args = args
        self.parsed_action = action 

        return self.PARSE_OK


    def get_parsed_cmd(self):
        return self.parsed_action, self.parsed_action_args



def get_tokens_from_raw_line(raw_line: str):
    line = raw_line.strip()
    if not line or line.startswith("#"):
        None, None

    parts = line.strip().split()
    if not parts:
        return None, []
    cmd_name = parts[0].upper()
    cmd_args = parts[1:]
    return cmd_name, cmd_args


def normalize_str(str_val):
    return str_val.upper()


def parse_command_args(action:Actions, cmd_args:list, cmd_arg_parsers:dict):    
    arg_parser = cmd_arg_parsers[action]
    parsed_args = arg_parser(cmd_args)
    return parsed_args


def check_first_arg_conv_to_float(args):
    if len(args) != 1:
        raise ValueError("Incorrect args count %s" % args)
    return float(args[0])


def check_no_args(args):
    if len(args) != 0:
        raise ValueError("Incorrect args count  %s" % args)

    return args


def check_if_the_only_arg_and_convert(conversion_func, args:list[str]):
    if len(args) != 1:
        raise ValueError("Incorrect args count %s" % args)
    
    arg_normalized = normalize_str(args[0])

    converted_val = conversion_func(arg_normalized)
    if converted_val is None: 
        raise ValueError("Incorrect argument provided %s" % (args[0]))

    return converted_val