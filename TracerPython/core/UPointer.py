from PIL import Image
from core.Point import Point
from core.DirectionEnum import Direction
import numpy as np

class UPointer:
	'''фактически Y растет вниз, X вправо, но названия даны для человеческого представления'''

	def pixel_is_inside_image(self, point: Point) -> bool:
		if (0 <= point.x < self.image.width) and (0 <= point.y < self.image.height):
			return True
		else: return False

	def position_is_available(self, position: Point) -> bool:
		if self.pixel_is_inside_image(position):
			return self.pixels[position.x, position.y]
		else: return False #TODO: ПРОВЕРИТЬ НЕ ПРИВОДИТ ЛИ ЭТО К ОШИБКАМ

	def get_color(self, point: Point):
		self.getting_pixels_count += 1
		if self.pixel_is_inside_image(point):
			# return self.image.getpixel((point.x, point.y))
			return self.image_pixels[point.x, point.y]

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

	def rotate_arrow(self, direction: Direction):
		if self.arrow == direction:
			self.arrow_is_changed = False
		else:
			self.arrow = direction
			self.arrow_is_changed = True

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

	def calc_arrow_strict(self):
		start_arrow = Direction.LEFT
		degrees = self.degrees_from_arrow(start_arrow) % 360
		for _ in range(0, 4):
			point = self.point_from_degress(self.pos, degrees)
			is_inside, is_same_color = self.check_inside_and_color(point)
			if is_inside and not is_same_color:
				return self.arrow_from_degrees(degrees + 90)
			degrees = (degrees + 90) % 360
		for _ in range(0, 4):
			point = self.point_from_degress(self.pos, degrees)
			if not self.position_is_available(point):
				return self.arrow_from_degrees(degrees + 90)
			degrees = (degrees + 90) % 360

	def calc_arrow(self, start_arrow=Direction.LEFT):
		degrees = start_arrow.value
		for _ in range(0, 4):
			point = self.point_from_degress(self.pos, degrees)
			is_inside, is_same_color = self.check_inside_and_color(point)
			if is_inside and not is_same_color:
				return self.arrow_from_degrees(degrees + 90)
			degrees = (degrees + 90) % 360
		for _ in range(0, 4):
			point = self.point_from_degress(self.pos, degrees)
			if not self.position_is_available(point):
				return self.arrow_from_degrees(degrees + 90)
			degrees = (degrees + 90) % 360
		raise Exception(f"impossible calc arrow, start_arrow = {start_arrow.name}, color = {self.color}, pos = {self.pos}")

	def pixel_is_strict_contour(self, point: Point):
		is_inside, is_same_color = self.check_inside_and_color(point)
		if not is_inside or not is_same_color: return False
		degrees = Direction.LEFT.value
		for _ in range(4):
			is_inside, is_same_color = self.check_inside_and_color(self.point_from_degress(point, degrees))
			if not is_inside or not is_same_color: return True
			# if is_inside and not is_same_color: return True
			degrees += 90
		return False

	def pixel_is_contour(self, point: Point) -> bool:
		is_inside, is_same_color = self.check_inside_and_color(point)
		if not is_inside or not is_same_color: return False
		degrees = Direction.LEFT.value
		for _ in range(4):
			is_inside, is_same_color = self.check_inside_and_color(self.point_from_degress(point, degrees))
			if not is_inside or not is_same_color: return True
			# if is_inside and not is_same_color: return True
			degrees += 90
		return False

	def set_start_position(self, point: Point):
		self.pos = point
		self.arrow = self.calc_arrow_strict()

	def calc_possible_position(self, arrow: Direction) -> tuple[Point, Direction]:
		degrees = (arrow.value - 90 + 360) % 360
		for _ in range(0, 8):
			point = self.point_from_degress(self.pos, degrees)
			if self.position_is_available(point) and self.pixel_is_contour(point):
				return (point, self.arrow_from_degrees(degrees))
			degrees = (degrees + 45) % 360
		return (self.pos,  arrow)

	def calc_possible_position_easy(self, arrow: Direction) -> tuple[Point, Direction]:
		degrees = (arrow.value - 90 + 360) % 360
		for _ in range(0, 8):
			point = self.point_from_degress(self.pos, degrees)
			_, is_same_color = self.check_inside_and_color(point)
			if self.position_is_available(point) and is_same_color:
				return (point, self.arrow_from_degrees(degrees))
			degrees = (degrees + 45) % 360
		return (self.pos,  arrow)

	def __init__(self, image: Image):
		self.image: Image = image
		width, height = image.size
		self.pixels = np.ones((width, height), dtype=bool)
		self.image_pixels = image.load()
		self.pos: Point = Point(0, 0)
		self.arrow: Direction = Direction.NONE
		self.arrow_is_changed: bool = False
		self.color: tuple = (0,0,0)

		self.moves_count: int = 0
		self.getting_pixels_count = 0
		self.getting_pixels_time = 0