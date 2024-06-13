from enum import Enum

class Directions(Enum):
	NONE = None
	UP = 0
	UP_RIGHT = 1
	RIGHT = 2 
	DOWN_RIGHT = 3
	DOWN = 4
	DOWN_LEFT = 5
	LEFT = 6
	UP_LEFT = 7

def rotate_clockwise(direction: Directions, value: int):
	return Directions((direction.value + value) % 8)

def rotate_counter_clockwise(direction: Directions, value: int):
	return Directions((direction.value - value + 8) % 8)

class ArrowSymbols:
    ARROWS = {
        Directions.UP.value: '↑',
        Directions.UP_RIGHT.value: '↗',
        Directions.RIGHT.value: '→',
        Directions.DOWN_RIGHT.value: '↘',
        Directions.DOWN.value: '↓',
        Directions.DOWN_LEFT.value: '↙',
		Directions.LEFT.value: '←',
        Directions.UP_LEFT.value: '↖',
    }