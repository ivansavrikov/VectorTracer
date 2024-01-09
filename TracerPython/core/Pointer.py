from typing import Tuple
from PIL import Image
from core.Point import Point
from core.ImagePreparer import ImagePreparer
from core.DirectionEnum import Direction


class Pointer:
    '''фактически Y растет вниз, X вправо, но названия даны в человеческом представлении'''

    def pixel_is_inside_image(self, point: Point) -> bool:
        width, height = self.image.size
        if (0 <= point.x < width) and (0 <= point.y < height): #Пиксель в пределах изображения
            return True
        else:
            return False

    def pixel_is_possible(self, point: Point) -> bool:
        if self.pixel_is_inside_image(point):
            if self.image.getpixel((point.x, point.y)) <= 100: #Яркость пикселя низкая (черный цвет)
                return True
            else:
                return False
        else:
            return False

    def move(self, point: Point) -> bool:
        if self.pixel_is_possible(point):
            self.pos = point
            self.moves_count += 1
            return True
        else:
            return False

    def move_left(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x-1, self.pos.y)), Direction.LEFT)

    def move_up_left(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x-1, self.pos.y-1)), Direction.UP_LEFT)

    def move_up(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x, self.pos.y-1)), Direction.UP)

    def move_up_right(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x+1, self.pos.y-1)), Direction.UP_RIGHT)

    def move_right(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x+1, self.pos.y)), Direction.RIGHT)
    
    def move_down_right(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x+1, self.pos.y+1)), Direction.DOWN_RIGHT)

    def move_down(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x, self.pos.y+1)), Direction.DOWN)

    def move_down_left(self) -> Tuple[bool, Direction]:
        return (self.move(Point(self.pos.x-1, self.pos.y+1)), Direction.DOWN_LEFT)

    def arrange_move_variants(self):
        match self.arrow:
            case Direction.RIGHT:
                self.move_variants = [self.move_up, 
                                      self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left]
                
            case Direction.DOWN_RIGHT:
                self.move_variants = [self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left, 
                                      self.move_up]
            
            case Direction.DOWN:
                self.move_variants = [self.move_right, 
                                      self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right]
            
            case Direction.DOWN_LEFT:
                self.move_variants = [self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right, 
                                      self.move_right]
            
            case Direction.LEFT:
                self.move_variants = [self.move_down, 
                                      self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right]
            
            case Direction.UP_LEFT:
                self.move_variants = [self.move_down_left, 
                                      self.move_left, 
                                      self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right, 
                                      self.move_down]
            
            case Direction.UP:
                self.move_variants = [self.move_left, 
                                      self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left]
            
            case Direction.UP_RIGHT:
                self.move_variants = [self.move_up_left, 
                                      self.move_up, 
                                      self.move_up_right, 
                                      self.move_right, 
                                      self.move_down_right, 
                                      self.move_down, 
                                      self.move_down_left, 
                                      self.move_left]
            case Direction.NONE:
                pass #сделать исключение или пустой список

    def rotate_arrow(self, direction: Direction):
        if self.arrow == direction:
            self.arrow_is_changed = False
        else:
            self.arrow = direction
            self.arrow_is_changed = True
            self.arrange_move_variants()

    def calculate_start_position(self, start: Point): #исключения продумать
        '''Вычисляет начальную точку контура фигуры'''

        width, height = self.image.size
        is_break = False
        for y in range(start.y, height):
            if is_break == True:
                break
            for x in range(start.x, width):
                point = Point(x, y)
                if self.pixel_is_possible(point):
                    self.pos = point
                    self.rotate_arrow(Direction.RIGHT) #
                    is_break = True
                    break

    def perform_move(self):
        for move in self.move_variants:
            has_moved, direction = move()
            if has_moved:
                self.rotate_arrow(direction)
                break

    def __init__(self, image: Image):
        self.image: Image = ImagePreparer.prepare(image)
        self.pos: Point = Point(0, 0)
        self.arrow: Direction = Direction.NONE
        self.arrow_is_changed: bool = True
        self.move_variants: list #Лист с функциями движения в нужном порядке
        self.moves_count = 0