class Point:
	def __init__(self, x: float, y: float):
		self.x: float = x
		self.y: float = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __truediv__(self, scalar):
		return Point(self.x / scalar, self.y / scalar)

	def __mul__(self, scalar):
		return Point(self.x * scalar, self.y * scalar)

	def round(self, decimals=0):
		return Point(round(self.x, decimals), round(self.y, decimals))

	def __repr__(self):
		return f"Point({self.x}, {self.y})"
	
	def length(self):
		return (self.x**2 + self.y**2)**0.5

	def normalize(self):
		length = self.length()
		return Point(self.x / length, self.y / length)