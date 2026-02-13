from cleaner import *

cleaner = init_cleaner(transfer_to_cleaner)
commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop']

new_cleaner = make(cleaner, commands)

print('position is:', new_cleaner.get_position())
print('direction is:', new_cleaner.get_direction())
print('device is:', new_cleaner.get_device())
