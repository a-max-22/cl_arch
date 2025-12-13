
import sys
import math
from enum import Enum


def calc_turn_by_given_degrees(angle:float, delta:float):
    return (angle + delta) % 360

def calc_position_change(angle:float, distance:float):
    rad = math.radians(angle)
    dx = math.cos(rad) * distance
    dy = math.sin(rad) * distance
    return dx, dy


def log(message:str):
    print(message)


def fmt_number(v):
    if v.is_integer():
        return str(int(v))
    return f"{v:.2f}".rstrip('0').rstrip('.')

