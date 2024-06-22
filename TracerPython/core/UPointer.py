from PIL import Image
from core.Point import Point
from core.Directions import Directions, rotate_clockwise, rotate_counter_clockwise
import numpy as np

class UPointer:
	'''фактически Y растет вниз, X вправо, но названия даны для человеческого представления'''

	def position_is_inside_image(self, point: Point) -> bool:
		if (0 <= point.x < self.image.width) and (0 <= point.y < self.image.height):
			return True
		else: return False

	def position_is_available(self, position: Point) -> bool:
		if self.position_is_inside_image(position):
			return self.available_positions[position.x, position.y]
		else: return False

	def get_color(self, point: Point):
		self.getting_pixels_count += 1
		if self.position_is_inside_image(point):
			return self.pixels[point.x, point.y]

	def check_inside_and_color(self, point: Point) -> tuple[bool, bool]:
		if self.position_is_inside_image(point):
			if self.get_color(point) == self.current_color:
				return (True, True)
			else: return (True, False)
		else: return (False, False)

	def rotate_direction(self, direction: Directions):
		if self.direction == direction:
			self.direction_is_changed = False
		else:
			self.direction = direction
			self.direction_is_changed = True

	def point_from_direction(self, point: Point, direction: Directions) -> Point:
		match(direction):
			case Directions.UP: return Point(point.x, point.y-1)
			case Directions.UP_RIGHT: return Point(point.x+1, point.y-1)
			case Directions.RIGHT: return Point(point.x+1, point.y)
			case Directions.DOWN_RIGHT: return Point(point.x+1, point.y+1)
			case Directions.DOWN: return Point(point.x, point.y+1)
			case Directions.DOWN_LEFT: return Point(point.x-1, point.y+1)
			case Directions.LEFT: return Point(point.x-1, point.y)
			case Directions.UP_LEFT: return Point(point.x-1, point.y-1)
		raise Exception(f"direction = {direction}")

	def calc_direction(self, direction=Directions.LEFT) -> Directions:
		for _ in range(0, 4):
			point = self.point_from_direction(self.position, direction)
			is_inside, is_same_color = self.check_inside_and_color(point)
			if is_inside and not is_same_color:
				return rotate_clockwise(direction, 2)
			direction = rotate_clockwise(direction, 2)
		for _ in range(0, 4):
			point = self.point_from_direction(self.position, direction)
			if not self.position_is_available(point):
				return rotate_clockwise(direction, 2)
			direction = rotate_clockwise(direction, 2)
		raise Exception(f"impossible calc arrow, start_arrow = {direction.name}, color = {self.current_color}, pos = {self.position}")

	def pixel_is_contour(self, point: Point, directions_count:int=4) -> bool:
		is_inside, is_same_color = self.check_inside_and_color(point)
		if not is_inside or not is_same_color: return False
		direction = Directions.LEFT
		for _ in range(directions_count):
			is_inside, is_same_color = self.check_inside_and_color(self.point_from_direction(point, direction))
			if not is_inside or not is_same_color: return True
			direction = rotate_clockwise(direction, 8/directions_count)
		return False

	def set_start_position(self, point: Point):
		self.position = point
		self.direction = self.calc_direction()

	def calc_possible_position(self, direction: Directions, directions_count=8) -> tuple[Point, Directions]:
		direction = rotate_counter_clockwise(direction, 2)
		for _ in range(0, directions_count):
			point = self.point_from_direction(self.position, direction)
			if self.position_is_available(point) and self.pixel_is_contour(point, 4):
				return (point, direction)
			direction = rotate_clockwise(direction, 8/directions_count)
		return (self.position,  direction)


	def __init__(self, image: Image):
		self.image: Image = image
		self.pixels = image.load()
		self.available_positions = np.ones((image.width, image.height), dtype=bool)
		self.position: Point = Point(0, 0)
		self.direction: Directions = Directions.NONE
		self.current_color: tuple = (0,0,0)
		self.direction_is_changed: bool = False	

		self.moves_count: int = 0
		self.getting_pixels_count = 0