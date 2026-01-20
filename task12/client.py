
from cleaner_api import RobotCommand, Setup, move, turn, set_state, start, stop

commands_list = [Setup()]
commands_list.append(RobotCommand(move, 100))
commands_list.append(RobotCommand(turn, -90))
commands_list.append(RobotCommand(set_state, "soap"))
commands_list.append(RobotCommand(start))
commands_list.append(RobotCommand(move, 50))
commands_list.append(RobotCommand(stop))

result = None
for c in commands_list:
    result = c.execute(result)
