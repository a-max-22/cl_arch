
import sys
import math


def fmt_number(v):
    if v.is_integer():
        return str(int(v))
    return f"{v:.2f}".rstrip('0').rstrip('.')


def calc_turn_by_given_degrees(angle:float, delta:float):
    return (angle + delta) % 360

def calc_position_change(angle:float, distance:float):
    rad = math.radians(angle)
    dx = math.cos(rad) * distance
    dy = math.sin(rad) * distance
    return dx, dy


def transfer_to_cleaner(message:str):
    print(message)

def log(message:str):
    print(message)

class RobotCleaner:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.device = "water"
        self.device_on = False


    def move(self, distance: float):
        dx, dy = calc_position_change(self.angle, distance)
        self.x += dx
        self.y += dy
        transfer_to_cleaner(f"POS {fmt_number(self.x)},{fmt_number(self.y)}")


    def turn(self, delta: float):
        self.angle = calc_turn_by_given_degrees(self.angle, delta)
        transfer_to_cleaner(f"ANGLE {round(self.angle, 2)}")


    def set_device(self, dev: str):
        dev = dev.lower()
        self.device = dev
        transfer_to_cleaner(f"STATE {self.device}")


    def start(self):
        self.device_on = True
        transfer_to_cleaner(f"START WITH {self.device}")


    def stop(self):
        self.device_on = False
        transfer_to_cleaner("STOP")



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


def parse_command_args(cmd_name:str, cmd_args:list, cmd_arg_parsers:dict):
    cmd_name_normalized = normalize_str(cmd_name)
    if cmd_name_normalized not in cmd_arg_parsers:
        raise ValueError("Unknown command %s" % cmd_name)
    
    arg_parser = cmd_arg_parsers[cmd_name_normalized]
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

def check_the_only_arg_in_list(allowed_list, args):
    if len(args) != 1:
        raise ValueError("Incorrect args count %s" % args)
    if args[0] not in allowed_list:
        raise ValueError("Arg is not allowed %s, has to be from %s" % (args[0], allowed_list))

    return args[0]


class CommandsParser:
    PARSE_OK  = 0
    PARSE_ERR = 1

    def __init__(self):
        self.parsed_command_name  = ''
        self.parsed_command_args  = ''

        self.VALID_DEVICES = {"water", "soap", "brush"}

        self.arg_parsers = {
            "MOVE" : lambda args:check_first_arg_conv_to_float(args),
            "TURN" : lambda args:check_first_arg_conv_to_float(args),
            "SET"  : lambda args:check_the_only_arg_in_list(self.VALID_DEVICES, args),
            "START": lambda args:check_no_args(args), 
            "STOP":  lambda args:check_no_args(args)
            }


    def parse_command(self, raw_line:str): 
        cmd_name, cmd_args = get_tokens_from_raw_line(raw_line)
        if cmd_name is None:
            return self.PARSE_ERR

        try:
            args = parse_command_args(cmd_name, cmd_args, self.arg_parsers)
        except ValueError as e:
            log(e)
            return self.PARSE_ERR
        
        self.parsed_command_args = args
        self.parsed_command_name = cmd_name 

        return self.PARSE_OK


    def get_parsed_cmd(self):
        return self.parsed_command_name, self.parsed_command_args



def run_command_handle(commands):
    robot = RobotCleaner()
    cmd_handlers  = {
        "MOVE" : lambda args: robot.move(args),
        "TURN" : lambda args: robot.turn(args),
        "SET"  : lambda args: robot.set_device(args),
        "START": lambda args: robot.start(),
        "STOP":  lambda args: robot.stop()
    }
    parser = CommandsParser()

    for raw_line in commands:
        if parser.parse_command(raw_line) != parser.PARSE_OK:
            continue

        cmd_name, cmd_args = parser.get_parsed_cmd()
        cmd_handlers[cmd_name](cmd_args)


def main():
    test_commands = [
    'MOVE 100',
    'TURN -90',
    'SET soap',
    'START',
    'MOVE 50',
    'STOP', 
    'SET brup', 
    'MOVE ',
    'START 00']
    run_command_handle(test_commands)



if __name__ == "__main__":

    main()
