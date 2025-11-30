import sys
import math


def fmt_number(v):
    if v.is_integer():
        return str(int(v))
    return f"{v:.2f}".rstrip('0').rstrip('.')


class RobotCleaner:
    VALID_DEVICES = {"water", "soap", "brush"}

    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.device = "water"
        self.device_on = False


    def move(self, distance: float):
        rad = math.radians(self.angle)
        dx = math.cos(rad) * distance
        dy = math.sin(rad) * distance
        self.x += dx
        self.y += dy
        print(f"POS {fmt_number(self.x)},{fmt_number(self.y)}")


    def turn(self, delta: float):
        self.angle = (self.angle + delta) % 360
        print(f"ANGLE {round(self.angle, 2)}")


    def set_device(self, dev: str):
        dev = dev.lower()
        if dev not in self.VALID_DEVICES:
            raise ValueError(f"Invalid device '{dev}'. Use water, soap or brush.")
        self.device = dev
        print(f"STATE {self.device}")


    def start(self):
        self.device_on = True
        print(f"START WITH {self.device}")


    def stop(self):
        self.device_on = False
        print("STOP")



def parse_line(line: str):
    parts = line.strip().split()
    if not parts:
        return None, []
    cmd = parts[0].upper()
    args = parts[1:]
    return cmd, args


def process_command(robot:RobotCleaner, cmd:str, args:list[str]):
    match cmd:
        case "MOVE":
            if len(args) != 1:
                raise ValueError("MOVE needs exactly one numeric argument.")
            dist = float(args[0])
            robot.move(dist)

        case "TURN":
            if len(args) != 1:
                raise ValueError("TURN needs exactly one numeric argument.")
            delta = float(args[0])
            robot.turn(delta)

        case "SET":
            if len(args) != 1:
                raise ValueError("SET needs exactly one argument (water/soap/brush).")
            robot.set_device(args[0])

        case "START":
            if args:
                raise ValueError("START takes no arguments.")
            robot.start()

        case "STOP":
            if args:
                raise ValueError("STOP takes no arguments.")
            robot.stop()

        case _:
            print(f"UNKNOWN COMMAND: {cmd}", file=sys.stderr)


def main():
    robot = RobotCleaner()
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        cmd, args = parse_line(line)
        if cmd is None:
            continue
        try:
            process_command(robot, cmd, args)
        except ValueError as e:
            print(e)
            continue


if __name__ == "__main__":
    main()