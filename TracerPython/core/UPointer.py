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

	def get_color(self, point: Point):
		if self.pixel_is_inside_image(point):
			return self.image.getpixel((point.x, point.y))

	def check_inside_and_color(self, point: Point) -> tuple[bool, bool]:
		if self.pixel_is_inside_image(point):
			if self.get_color(point) == self.color:
				return (True, True)
			else: return (True, False)
		else: return (False, False)

	def pixel_is_possible(self, point: Point) -> bool:
		if self.pixel_is_inside_image(point):
			if self.get_color(point) == self.color:
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
				raise MyCustomException("Direction == None")
				#TODO: Здесь тупик

	def rotate_arrow(self, direction: Direction):
		if self.arrow == direction:
			self.arrow_is_changed = False
		else:
			self.arrow = direction
			self.arrow_is_changed = True
			self.arrange_move_variants()

	def arrow_from_degrees(self, degrees: int) -> Direction:
		degrees = degrees % 360
		match(degrees):
			case 0: return Direction.LEFT
			case 45: return Direction.UP_LEFT
			case 90: return Direction.UP
			case 135: return Direction.UP_RIGHT
			case 180: return Direction.RIGHT
			case 225: return Direction.DOWN_RIGHT
			case 270: return Direction.DOWN
			case 315: return Direction.DOWN_LEFT
			case 360: return Direction.LEFT
		raise Exception(f"Что-то не так с градусами: {degrees}")
	
	def degrees_from_arrow(self, direction: Direction) -> int:
		match(direction):
			case Direction.LEFT: return 0
			case Direction.UP_LEFT: return 45
			case Direction.UP: return 90
			case Direction.UP_RIGHT: return 135
			case Direction.RIGHT: return 180
			case Direction.DOWN_RIGHT: return 225
			case Direction.DOWN: return 270
			case Direction.DOWN_LEFT: return 315
		raise Exception(f"Что-то не так со стрелкой: {direction}")

	def point_from_arrow(self, point: Point, direction: Direction) -> Point:
		match(direction):
			case Direction.LEFT: return Point(point.x-1, point.y)
			case Direction.UP_LEFT: return Point(point.x-1, point.y-1)
			case Direction.UP: return Point(point.x, point.y-1)
			case Direction.UP_RIGHT: return Point(point.x+1, point.y-1)
			case Direction.RIGHT: return Point(point.x+1, point.y)
			case Direction.DOWN_RIGHT: return Point(point.x+1, point.y+1)
			case Direction.DOWN: return Point(point.x, point.y+1)
			case Direction.DOWN_LEFT: return Point(point.x-1, point.y+1)
		raise Exception(f"direction = {direction}")

	def point_from_degress(self, point: Point, degrees: int):
		match(degrees):
			case 0: return Point(point.x-1, point.y)
			case 45: return Point(point.x-1, point.y-1)
			case 90: return Point(point.x, point.y-1)
			case 135: return Point(point.x+1, point.y-1)
			case 180: return Point(point.x+1, point.y)
			case 225: return Point(point.x+1, point.y+1)
			case 270: return Point(point.x, point.y+1)
			case 315: return Point(point.x-1, point.y+1)

	def calc_start_arrow_simple(self) -> Direction:
		left = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.LEFT))
		up_left = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.UP_LEFT))
		up = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.UP))
		up_right = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.UP_RIGHT))

		right = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.RIGHT))
		down_right = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.DOWN_RIGHT))
		down = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.DOWN))
		down_left = self.pixel_is_possible(self.point_from_arrow(self.pos, Direction.DOWN_LEFT))

		if not left: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.LEFT) + 90)
		elif not up_left: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.UP_LEFT) + 90)
		elif not up: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.UP) + 90)
		elif not up_right: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.UP_RIGHT) + 90)
		
		elif not right: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.RIGHT) + 90)
		elif not down_right: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.DOWN_RIGHT) + 90)
		elif not down: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.DOWN) + 90)
		elif not down_left: return self.arrow_from_degrees(self.degrees_from_arrow(Direction.DOWN_LEFT) + 90)

		# else: return Direction.NONE
		raise Exception("Не получается определить начальное направление")

	def calc_arrow(self, start_arrow=Direction.LEFT):
		degrees = self.degrees_from_arrow(start_arrow) % 360
		for _ in range(0, 4):
			if not self.pixel_is_possible(self.point_from_degress(self.pos, degrees)):
				return self.arrow_from_degrees(degrees + 90)
			degrees = (degrees + 90) % 360
		# print(f"impossible calc arrow, start_arrow = {start_arrow.name}")
		raise Exception(f"impossible calc arrow, start_arrow = {start_arrow.name}, color = {self.color}, pos = {self.pos}")

	def calc_clockwise(self) -> bool:
		if (
			self.arrow == Direction.UP_LEFT or 
			self.arrow == Direction.UP or 
			self.arrow == Direction.UP_RIGHT or 
			self.arrow == Direction.RIGHT
		):
			return True
		elif (
			self.arrow == Direction.LEFT or 
			self.arrow == Direction.DOWN_LEFT or 
			self.arrow == Direction.DOWN or 
			self.arrow == Direction.DOWN_RIGHT
		):
			return True

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
				# print(f'case 0 : {self.pos}, {self.arrow.value}')
				return False
			case 1:
				if not up_true_px: self.rotate_arrow(Direction.DOWN_RIGHT)
				elif not down_true_px: self.rotate_arrow(Direction.UP_LEFT)
				elif not left_true_px: self.rotate_arrow(Direction.UP_RIGHT)
				elif not right_true_px: self.rotate_arrow(Direction.DOWN_LEFT)
				# print(f'case 1 : {self.pos}, {self.arrow.value}')
				return True

			case 2:
				if not up_true_px and not right_true_px: self.rotate_arrow(Direction.DOWN_LEFT)
				elif not up_true_px and not left_true_px: self.rotate_arrow(Direction.DOWN_RIGHT)
				elif not down_true_px and not left_true_px: self.rotate_arrow(Direction.UP_RIGHT)
				elif not down_true_px and not right_true_px: self.rotate_arrow(Direction.UP_LEFT)
				elif not up_true_px and not down_true_px: self.rotate_arrow(Direction.UP_LEFT) #
				elif not left_true_px and not right_true_px: self.rotate_arrow(Direction.UP_RIGHT) #
				# print(f'case 2 : {self.pos}, {self.arrow.value}')
				return True
			
			case 3:
				if not up_true_px and not left_true_px and not right_true_px: self.rotate_arrow(Direction.DOWN) #
				if not up_true_px and not down_true_px and not right_true_px: self.rotate_arrow(Direction.LEFT)
				if not down_true_px and not left_true_px and not right_true_px: self.rotate_arrow(Direction.UP)
				if not up_true_px and not down_true_px and not left_true_px: self.rotate_arrow(Direction.RIGHT)
				# print(f'case 3 : {self.pos}, {self.arrow.value}')
				return True
		
		self.pos = start
	
	def pixel_is_contour(self, point: Point) -> bool:
		# left = self.pixel_is_possible(self.point_from_arrow(point, Direction.LEFT))
		# up = self.pixel_is_possible(self.point_from_arrow(point, Direction.UP))
		# right = self.pixel_is_possible(self.point_from_arrow(point, Direction.RIGHT))
		# down = self.pixel_is_possible(self.point_from_arrow(point, Direction.DOWN))

		# if not left or not up or not right or not down:
		# 	return True
		# else:
		# 	return False
		
		degrees = Direction.LEFT.value
		for _ in range(4):
			is_inside, is_same_color = self.check_inside_and_color(self.point_from_degress(point, degrees))
			if not is_inside or not is_same_color: return True
			# if is_inside and not is_same_color: return True
			degrees += 90
		return False


	def calculate_start_position(self, start: Point, end: Point) -> bool: #исключениsя продумать
		'''Вычисляет начальную точку контура фигуры'''
		for y in range(start.y, end.y+1):
			for x in range(start.x, end.x+1):
				point = Point(x, y)
				if self.pixel_is_possible(point):
					if self.pixel_is_contour(point):
						self.pos = point
						self.moves_count += 1
						self.rotate_arrow(self.calc_start_arrow_simple())
						return True
		return False

	def calc_possible_position(self, arrow: Direction) -> tuple[Point, Direction]:
		degrees = (self.degrees_from_arrow(arrow) - 90 + 360) % 360
		for _ in range(0, 8):
			if self.pixel_is_possible(self.point_from_degress(self.pos, degrees)):
				return (self.point_from_degress(self.pos, degrees), self.arrow_from_degrees(degrees))
			degrees = (degrees + 45) % 360
		return (self.pos,  arrow)

	def set_position_auto(self):
		possible_position, possible_arrow = self.calc_possible_position(self.arrow)
		recalc_arrow = possible_arrow
		# while True:
		# 	if possible_position.x != self.pos.x and possible_position.y != self.pos.y:
		# 		if self.get_color(Point(possible_position.x, self.pos.y)) == self.get_color(Point(self.pos.x, possible_position.y)):
		# 			if recalc_arrow.value % 90 != 0: recalc_arrow = self.arrow_from_degrees(recalc_arrow.value + 45)
		# 			recalc_arrow = self.calc_arrow(recalc_arrow)
		# 			possible_position, recalc_arrow = self.calc_possible_position(recalc_arrow)
		# 			if recalc_arrow == possible_arrow:
		# 				break
		# 		else: break
		# 	else: break

			# print(f'{self.arrow.name} -> {possible_arrow.name} color={self.color} pos={self.pos}')

		self.pos = possible_position
		self.rotate_arrow(recalc_arrow)
		self.moves_count += 1
		return True

	def perform_move_universal(self):
		degrees = (self.degrees_from_arrow(self.arrow) - 90 + 360) % 360
		for _ in range(0, 8):
			if self.try_move(self.point_from_degress(self.pos, degrees)):
				self.rotate_arrow(self.arrow_from_degrees(degrees))
				return
			degrees = (degrees + 45) % 360

	def perform_move(self):
		nope = 0
		for move in self.move_variants:
			#для того чтобы указатель мог двигаться только влево вправо вниз и вверх
			# if (
			# 	move != self.move_up_left and
			# 	move != self.move_up_right and
			# 	move != self.move_down_left and
			# 	move != self.move_down_right
			# ):
			has_moved, direction = move()
			if has_moved:
				self.rotate_arrow(direction)
				return
			else:
				nope += 1

		# if nope == 8 or len(self.move_variants) == 0:
		# 	raise MyCustomException(f'нельзя двигаться: nope = {nope}, move_vars = {len(self.move_variants)}, {self.color}, x,y = {self.pos.x}, {self.pos.y}')

	def __init__(self, image: Image):
		self.image: Image = image
		self.pos: Point = Point(0, 0)
		self.arrow: Direction = Direction.NONE
		self.arrow_is_changed: bool = False
		self.move_variants: list = [] #Лист с функциями движения в нужном порядке
		self.moves_count: int = 0
		self.color: tuple = (0,0,0)