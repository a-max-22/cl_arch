
def transfer_to_robot(message):
    pass

def robot_move(dist):
    message = 'move %d' % dist
    transfer_to_robot(message)

def robot_turn(angle):
    message = 'turn %d' % angle
    transfer_to_robot(message)

def robot_set(device):
    message = 'set %d' % device
    transfer_to_robot(message)

def robot_start():
    message = 'start'
    transfer_to_robot(message)


def robot_stop():
    message = 'stop'
    transfer_to_robot(message)
