from PIL import Image
import numpy
import math
from core.Point import Point

def is_inside(point: Point, shape: tuple[int, int]) -> bool:
	width, height = shape
	if (0 <= point.x < width) and (0 <= point.y < height): return True
	else: return False

def optimaze(image: Image, available_positions: numpy.ndarray):
	square_size = 5
	image_width, image_height = image.size
	pixels = image.load()
	
	width_fragments: int = math.ceil(image_width/square_size) #ширина изображения в фрагментах
	height_fragments: int = math.ceil(image_height/square_size) #высота изображения в фрагментах

	for hf in range(height_fragments):
		for wf in range(width_fragments):
			square_position = Point(wf*square_size, hf*square_size)	
			color = pixels[square_position.x, square_position.y]
			square_is_truncated = False
			square_is_solid = True
			is_break = False
			for y in range(square_position.y, square_position.y + square_size):
				if is_break: break
				for x in range(square_position.x, square_position.x + square_size):
					point: Point = Point(x, y)
					if is_inside(point, image.size):
						if pixels[point.x, point.y] != color:
							square_is_solid = False
							is_break == True
							break
					else:
						square_is_truncated = True

			if square_is_solid and not square_is_truncated:
				if scaled_square_is_solid(pixels, square_position, square_size, color, image.size):
					for y in range(square_position.y, square_position.y+square_size):
						for x in range(square_position.x, square_position.x + square_size):
							available_positions[x, y] = False
				else:
					for y in range(square_position.y+1, square_position.y+1+square_size-2):
						for x in range(square_position.x+1, square_position.x+1 + square_size-2):
							available_positions[x, y] = False


def scaled_square_is_solid(pixels, square_position, square_size, color, size) -> bool:
	square_size = square_size+2
	square_position = Point(square_position.x-1, square_position.y-1)
	
	# Верхний ряд (включая последний элемент)
	for x in range(square_position.x, square_position.x + square_size):
		point = Point(x, square_position.y)
		if is_inside(point, size):
			if pixels[point.x, point.y] != color: return False
		else: return False
	
	# Правый столбец (включая последний элемент)
	for y in range(square_position.y + 1, square_position.y + square_size):
		point = Point(square_position.x + square_size - 1, y)
		if is_inside(point, size):
			if pixels[point.x, point.y] != color: return False
		else: return False

	# Нижний ряд (включая первый элемент, но исключая последний, так как уже включен в правый столбец)
	for x in range(square_position.x + square_size - 2, square_position.x - 1, -1):
		point = Point(x, square_position.y + square_size - 1)
		if is_inside(point, size):
			if pixels[point.x, point.y] != color: return False
		else: return False

	# Левый столбец (включая первый элемент, но исключая последний, так как уже включен в верхний ряд)
	for y in range(square_position.y + square_size - 2, square_position.y, -1):
		point = Point(square_position.x, y)
		if is_inside(point, size):
			if pixels[point.x, point.y] != color: return False
		else: return False

	return True