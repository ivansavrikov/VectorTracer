from typing import Tuple
from PIL import Image
from core.Point import Point
from core.ImagePreparer import ImagePreparer
from core.DirectionEnum import Direction


class Pointer:
    '''фактически Y растет вниз, X вправо, но названия даны в человеческом представлении'''

    #Возможно есть ошибка
    def point_is_inside_area(point: Point, start: Point, end: Point) -> bool:
        '''Проверяет входит ли точка в квадратную область start=леваяверхняя координата, end=праваянижняя'''
        if (
            point.x >= start.x and
            point.x <= end.x and
            point.y >= start.y and
            point.y <= end.y
        ):
            return True
        else:
            return False

    def pixel_is_inside_image(self, point: Point) -> bool:
        width, height = self.image.size
        if (0 <= point.x < width) and (0 <= point.y < height): #Пиксель в пределах изображения
            return True
        else:
            return False

    def pixel_is_possible(self, point: Point, lumi:int = 0) -> bool:
        if self.pixel_is_inside_image(point):
            if self.image.getpixel((point.x, point.y)) == lumi: #== lumi
                return True
            else:
                return False
        else:
            return False

    def move(self, point: Point) -> bool:
        # if self.pixel_is_possible(point, self.trace_color):
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
                self.move_variants = []
                pass #сделать исключение или пустой список

    def rotate_arrow(self, direction: Direction):
        if self.arrow == direction:
            self.arrow_is_changed = False
        else:
            self.arrow = direction
            self.arrow_is_changed = True
            self.arrange_move_variants()

    def calculate_start_position(self, start: Point, end: Point, is_white: bool=False): #исключения продумать
        '''Вычисляет начальную точку контура фигуры'''

        if is_white:
            self.trace_color = 255
        else:
            self.trace_color = 0

        prev = start
        is_break = False
        for y in range(start.y, end.y+1):
            if is_break == True:
                break
            for x in range(start.x, end.x+1):
                point = Point(x, y)
                if self.pixel_is_possible(point, self.trace_color):

                    if self.trace_color == 0:
                        self.pos = point
                        self.rotate_arrow(Direction.RIGHT) #
                    elif self.trace_color == 255:
                        self.pos = prev
                        self.rotate_arrow(Direction.LEFT) #

                    # self.pos = point
                    # self.rotate_arrow(Direction.RIGHT) #
                    is_break = True
                    break
                prev = point

    def perform_move(self):
        nope = 0
        for move in self.move_variants:
            
            #для того чтобы указатель мог двигаться только влево вправо вниз и вверх
            # if (
            #     move != self.move_up_left and
            #     move != self.move_up_right and
            #     move != self.move_down_left and
            #     move != self.move_down_right
            # ):
                
            has_moved, direction = move()
            if has_moved:
                self.rotate_arrow(direction)
                break
            else:
                nope += 1


        # if nope == 8 or len(self.move_variants) == 0:
        #     print(f'нельзя двигаться: nope = {nope}, move_vars = {len(self.move_variants)}, {self.trace_color}, x,y = {self.pos.x}, {self.pos.y}')

    def __init__(self, image: Image):
        self.image: Image = ImagePreparer.prepare(image)
        self.pos: Point = Point(0, 0)
        self.arrow: Direction = Direction.NONE
        self.arrow_is_changed: bool = False
        self.move_variants: list = [] #Лист с функциями движения в нужном порядке
        self.moves_count: int = 0
        self.trace_color: int = 0 #трассировка черной фигуры, 255 - белой