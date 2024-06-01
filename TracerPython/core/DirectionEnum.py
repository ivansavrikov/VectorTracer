from enum import Enum

class Direction(Enum):
	NONE = None
	LEFT = 0
	UP_LEFT = 45
	UP = 90
	UP_RIGHT = 135
	RIGHT = 180 
	DOWN_RIGHT = 225
	DOWN = 270
	DOWN_LEFT = 315

class ArrowSymbols:
    ARROWS = {
        0: '←',
        45: '↖',
        90: '↑',
        135: '↗',
        180: '→',
        225: '↘',
        270: '↓',
        315: '↙'
    }