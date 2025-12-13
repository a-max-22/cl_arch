
from RobotCleaner import RobotCleaner, Actions
from CommandParser import CommandsParser



def run_commands_interpreter(commands):
    robot = RobotCleaner()
    cmd_handlers  = {
        Actions.MOVE  : lambda args: robot.move(args),
        Actions.TURN  : lambda args: robot.turn(args),
        Actions.SET   : lambda args: robot.set_device(args),
        Actions.START : lambda args: robot.start(),
        Actions.STOP  : lambda args: robot.stop()
    }
    parser = CommandsParser()

    for raw_line in commands:
        if parser.parse_command(raw_line) != parser.PARSE_OK:
            continue

        action, args = parser.get_parsed_cmd()
        cmd_handlers[action](args)


def main():
    test_commands = [
    'MOVE 100',
    'TURN -90',
    'SET soap',
    'START',
    'SPVART',
    'MOVE 50',
    'STOP', 
    'SET brup', 
    'MOVE ',
    'START 00']
    run_commands_interpreter(test_commands)



if __name__ == "__main__":
    main()