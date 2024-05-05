from typing import Tuple
from PIL import Image
from core.Point import Point
from core.ImagePreparer import ImagePreparer
from core.DirectionEnum import Direction
from core.Exceptions import MyCustomException
from core.Console import Console

class UPointer:
    '''фактически Y растет вниз, X вправо, но названия даны для человеческого представления'''

    def pixel_is_inside_image(self, point: Point) -> bool:
        width, height = self.image.size
        if (0 <= point.x < width) and (0 <= point.y < height): #Пиксель в пределах изображения
            return True
        else: return False

    def pixel_is_possible(self, point: Point) -> bool:
        if self.pixel_is_inside_image(point):
            if self.image.getpixel((point.x, point.y)) == self.color:
                return True
            else: return False
        else: return False

    def try_move(self, point: Point) -> bool:
        if self.pixel_is_possible(point):
            self.pos = point
            self.moves_count += 1
            return True
        else:
            return False

    def move_left(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x-1, self.pos.y)), Direction.LEFT)

    def move_up_left(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x-1, self.pos.y-1)), Direction.UP_LEFT)

    def move_up(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x, self.pos.y-1)), Direction.UP)

    def move_up_right(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x+1, self.pos.y-1)), Direction.UP_RIGHT)

    def move_right(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x+1, self.pos.y)), Direction.RIGHT)
    
    def move_down_right(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x+1, self.pos.y+1)), Direction.DOWN_RIGHT)

    def move_down(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x, self.pos.y+1)), Direction.DOWN)

    def move_down_left(self) -> Tuple[bool, Direction]:
        return (self.try_move(Point(self.pos.x-1, self.pos.y+1)), Direction.DOWN_LEFT)

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
                raise MyCustomException("Directtion == None")
                #TODO: Здесь тупик

    def rotate_arrow(self, direction: Direction):
        if self.arrow == direction:
            self.arrow_is_changed = False
        else:
            self.arrow = direction
            self.arrow_is_changed = True
            self.arrange_move_variants()

    def calc_start_arrow(self) -> bool:
        start = self.pos
        false_px_count = 0

        up_true_px, _ = self.move_up()
        self.pos = start
        down_true_px, _ = self.move_down()
        self.pos = start
        left_true_px, _ = self.move_left()
        self.pos = start
        right_true_px, _ = self.move_right()
        self.pos = start

        if not up_true_px: false_px_count += 1
        if not down_true_px: false_px_count += 1
        if not left_true_px: false_px_count += 1
        if not right_true_px: false_px_count += 1
        
        match false_px_count:
            case 0:
                # print('case 0') 
                return False
            case 1:
                # print('case 1')
                if not up_true_px: self.rotate_arrow(Direction.DOWN_RIGHT)
                elif not down_true_px: self.rotate_arrow(Direction.UP_LEFT)
                elif not left_true_px: self.rotate_arrow(Direction.UP_RIGHT)
                elif not right_true_px: self.rotate_arrow(Direction.DOWN_LEFT)
                return True

            case 2:
                # print('case 2')
                if not up_true_px and not right_true_px: self.rotate_arrow(Direction.DOWN_LEFT)
                elif not up_true_px and not left_true_px: self.rotate_arrow(Direction.DOWN_RIGHT)
                elif not down_true_px and not left_true_px: self.rotate_arrow(Direction.UP_RIGHT)
                elif not down_true_px and not right_true_px: self.rotate_arrow(Direction.UP_LEFT)
                elif not up_true_px and not down_true_px: self.rotate_arrow(Direction.UP_LEFT) #
                elif not left_true_px and not right_true_px: self.rotate_arrow(Direction.UP_RIGHT) #
                return True
            
            case 3:
                # print('case 3')
                if not up_true_px and not left_true_px and not right_true_px: self.rotate_arrow(Direction.DOWN) #
                if not up_true_px and not down_true_px and not right_true_px: self.rotate_arrow(Direction.LEFT)
                if not down_true_px and not left_true_px and not right_true_px: self.rotate_arrow(Direction.UP)
                if not up_true_px and not down_true_px and not left_true_px: self.rotate_arrow(Direction.RIGHT)
                return True
        
        self.pos = start
        

    def calculate_start_position(self, start: Point, end: Point): #исключениsя продумать
        '''Вычисляет начальную точку контура фигуры'''
        for y in range(start.y, end.y+1):
            for x in range(start.x, end.x+1):
                point = Point(x, y)
                if self.try_move(point):
                    if self.calc_start_arrow():
                        return

    def perform_move(self):
        nope = 0
        for move in self.move_variants:
            has_moved, direction = move()
            if has_moved:
                self.rotate_arrow(direction)
                return
            else:
                nope += 1

        # if nope == 8 or len(self.move_variants) == 0:
        #     raise MyCustomException(f'нельзя двигаться: nope = {nope}, move_vars = {len(self.move_variants)}, {self.color}, x,y = {self.pos.x}, {self.pos.y}')

    def __init__(self, image: Image):
        self.image: Image = image
        self.pos: Point = Point(0, 0)
        self.arrow: Direction = Direction.NONE
        self.arrow_is_changed: bool = False
        self.move_variants: list = [] #Лист с функциями движения в нужном порядке
        self.moves_count: int = 0
        self.color: tuple = (0,0,0)