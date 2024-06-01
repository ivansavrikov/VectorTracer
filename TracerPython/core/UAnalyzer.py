from PIL import Image
from core.UFragment import UFragment
from core.Point import Point
from core.UPointer import UPointer
from typing import List
import math
from core.Console import Console as C
from core.FragmentAnalyzer import FragmentAnalyzer
import time

class UAnalyzer:				

	def point_is_inside(fragment: UFragment, point: Point) -> bool:
		'''Проверяет входит ли точка во фрагмент'''
		if (
			point.x >= fragment.position.x and
			point.x <= fragment.position.x + UFragment.size - 1 and
			point.y >= fragment.position.y and
			point.y <= fragment.position.y + UFragment.size - 1
		):
			return True
		else:
			return False

	def analyze(image: Image):
		analyzing_time = 0
		fragment_analyzer = FragmentAnalyzer(image)
		
		fragments = dict()
		width_fragments: int = math.ceil(image.width/UFragment.size) #ширина изображения в фрагментах
		height_fragments: int = math.ceil(image.height/UFragment.size) #высота изображения в фрагментах

		pointer: UPointer = UPointer(image)

		i = 0
		for hf in range(height_fragments):
			for wf in range(width_fragments):
				fragment = UFragment()
				fragment.index = i
				fragment.position = Point(wf*UFragment.size, hf*UFragment.size)
				
				colors = dict()
				is_outside_image = False
				#анализ фрагмента на 1 пиксель больше исходного
				for y in range(fragment.position.y-1, fragment.position.y + UFragment.size + 1): 
					for x in range(fragment.position.x-1, fragment.position.x + UFragment.size + 1):
				# for y in range(fragment.position.y, fragment.position.y + UFragment.size):
				# 	for x in range(fragment.position.x, fragment.position.x + UFragment.size):
						point: Point = Point(x, y)
						if pointer.pixel_is_inside_image(point): #Пиксель в пределах изображения
							r, g, b = image.getpixel((point.x, point.y))
							color = f"{r},{g},{b}"
							if color not in colors:
								colors[color] = 1
							if UAnalyzer.point_is_inside(fragment, point):
								if color not in fragment.colors:	
									fragment.colors[color] = 1
								else:
									fragment.colors[color] += 1
						else:
							is_outside_image = True


				if len(colors) > 1 or is_outside_image:
					start_time = time.time()
					fragment_analyzer.Analyze(fragment)
					end_time = time.time()
					analyzing_time += end_time - start_time
					fragments[fragment.index] = fragment

				i += 1

		print(analyzing_time)
		return fragments