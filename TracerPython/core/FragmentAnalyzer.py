from PIL import Image
import numpy as np
from core.UFragment import UFragment
from core.UPointer import UPointer
from core.Point import Point

class FragmentAnalyzer:
	def __init__(self, image: Image) -> None:
		self.image = image
		self.main_pointer = UPointer(image)

	def Analyze(self, f: UFragment):
		croped_image = self.image.crop((f.position.x, f.position.y, f.position.x + f.size, f.position.y  + f.size))
		pointer = UPointer(croped_image)
		f_pixels = np.array(croped_image)
		pixels = np.ma.array(f_pixels)
		pixels.mask = False

		for y in range(f_pixels.shape[0]):  # Перебор строк
			for x in range(f_pixels.shape[1]):  # Перебор столбцов
				global_point = Point(f.position.x + x, f.position.y + y)
				rgb = pixels[y][x]
				pointer.color = (rgb[0], rgb[1], rgb[2])
				self.main_pointer.color = (rgb[0], rgb[1], rgb[2])
				if pointer.pixel_is_possible(Point(x, y)):
					if self.main_pointer.pixel_is_contour(global_point):
						key_point = f'{global_point.x},{global_point.y}'
						f.start_points[key_point] = pointer.color
						f.virgin_points[key_point] = True

		# pixels.mask[x, y] = True
		return croped_image


