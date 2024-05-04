from enum import Enum

class Direction(Enum):
    NONE = 'None'
    RIGHT = '→'
    DOWN_RIGHT = '↘'
    DOWN = '↓'
    DOWN_LEFT = '↙'
    LEFT = '←'
    UP_LEFT = '↖'
    UP = '↑'
    UP_RIGHT = '↗'