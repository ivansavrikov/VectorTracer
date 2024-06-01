from core.Point import Point



class UFragment:
	'''Данные Квадратного фрагмента изображения'''

	size: int = 16

	def __init__(self):
		self.index = 0
		self.position: Point
		self.colors: dict = dict()
		self.start_points = dict()

		self.virgin_points = dict()