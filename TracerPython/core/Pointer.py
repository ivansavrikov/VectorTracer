from typing import Tuple
from PIL import Image
from enum import Enum

class Direction(Enum): #Directions
    NONE = 'None'
    RIGHT = 'Right'
    DOWN_RIGHT = 'Down_Right'
    DOWN = 'Down'
    DOWN_LEFT = 'Down_Left'
    LEFT = 'Left'
    UP_LEFT = 'Up_Left'
    UP = 'Up'
    UP_RIGHT = 'Up_Right'

class Pointer:

    def pixel_is_possible(self, xy: Tuple[int, int]) -> bool:
        x, y = xy
        width, height = self.image.size
        if (0 <= x < width) and (0 <= y < height): #Пиксель в пределах изображения
            if self.image.getpixel(xy) <= 1: #Яркость пикселя низкая (черный цвет)
                return True
            else:
                return False
        else:
            return False

    def move(self, xy: Tuple[int, int]) -> bool:
        if self.pixel_is_possible(xy):
            self.x, self.y = xy
            self.moves_count += 1
            return True
        else:
            return False

    def move_left(self) -> Tuple[bool, Direction]:
        return (self.move((self.x-1, self.y)), Direction.LEFT)

    def move_up_left(self) -> Tuple[bool, Direction]:
        return (self.move((self.x-1, self.y-1)), Direction.UP_LEFT)

    def move_up(self) -> Tuple[bool, Direction]:
        return (self.move((self.x, self.y-1)), Direction.UP)

    def move_up_right(self) -> Tuple[bool, Direction]:
        return (self.move((self.x+1, self.y-1)), Direction.UP_RIGHT)

    def move_right(self) -> Tuple[bool, Direction]:
        return (self.move((self.x+1, self.y)), Direction.RIGHT)
    
    def move_down_right(self) -> Tuple[bool, Direction]:
        return (self.move((self.x+1, self.y+1)), Direction.DOWN_RIGHT)

    def move_down(self) -> Tuple[bool, Direction]:
        return (self.move((self.x, self.y+1)), Direction.DOWN)

    def move_down_left(self) -> Tuple[bool, Direction]:
        return (self.move((self.x-1, self.y+1)), Direction.DOWN_LEFT)

    def arrange_move_variants(self):
        match self.arrow:
            case Direction.RIGHT:
                self.move_variants = [self.move_up, self.move_up_right, self.move_right, self.move_down_right, self.move_down, self.move_down_left, self.move_left, self.move_up_left]
            case Direction.DOWN_RIGHT:
                self.move_variants = [self.move_up_right, self.move_right, self.move_down_right, self.move_down, self.move_down_left, self.move_left, self.move_up_left, self.move_up]
            case Direction.DOWN:
                self.move_variants = [self.move_right, self.move_down_right, self.move_down, self.move_down_left, self.move_left, self.move_up_left, self.move_up, self.move_up_right]
            case Direction.DOWN_LEFT:
                self.move_variants = [self.move_down_right, self.move_down, self.move_down_left, self.move_left, self.move_up_left, self.move_up, self.move_up_right, self.move_right]
            case Direction.LEFT:
                self.move_variants = [self.move_down, self.move_down_left, self.move_left, self.move_up_left, self.move_up, self.move_up_right, self.move_right, self.move_down_right]
            case Direction.UP_LEFT:
                self.move_variants = [self.move_down_left, self.move_left, self.move_up_left, self.move_up, self.move_up_right, self.move_right, self.move_down_right, self.move_down]
            case Direction.UP:
                self.move_variants = [self.move_left, self.move_up_left, self.move_up, self.move_up_right, self.move_right, self.move_down_right, self.move_down, self.move_down_left]
            case Direction.UP_RIGHT:
                self.move_variants = [self.move_up_left, self.move_up, self.move_up_right, self.move_right, self.move_down_right, self.move_down, self.move_down_left, self.move_left]
            case Direction.NONE:
                pass #сделать исключение или пустой список

    def rotate_arrow(self, direction: Direction):
        if self.arrow == direction:
            self.arrow_is_changed = False
        else:
            self.arrow = direction
            self.arrow_is_changed = True
            self.arrange_move_variants()
            # print(f'Направление изменилось {self.arrow.value}')

    def calculate_start_position(self, xy: Tuple[int, int]): #исключения продумать
        width, height = self.image.size
        start_x, start_y = xy
        is_break = False
        for y in range(start_y, height):
            if is_break == True:
                break
            for x in range(start_x, width):
                if self.pixel_is_possible((x, y)):
                    self.x = x
                    self.y = y
                    self.rotate_arrow(Direction.RIGHT)
                    is_break = True
                    break

    def perform_move(self):
        for move in self.move_variants:
            has_moved, direction = move()
            if has_moved:
                self.rotate_arrow(direction)
                break

    def __init__(self, image: Image):
        self.image: Image = image.convert('L')
        self.x: int
        self.y: int
        self.arrow: Direction = Direction.NONE
        self.arrow_is_changed: bool = True
        self.move_variants: list #Лист с функциями движения в нужном порядке
        self.moves_count = 0
        self.calculate_start_position((0,0)) #начинаем двигаться с нулевых координат