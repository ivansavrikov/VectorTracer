from core.Point import Point



class Fragment:
    '''Данные Квадратного фрагмента изображения'''

    def __init__(self):
        size = 32
        self.width = size
        self.height = size

        self.index: int
        self.position: Point
        self.is_edge: bool = False
        self.black_count: int = 0