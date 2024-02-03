from core.Point import Point



class Fragment:
    '''Данные Квадратного фрагмента изображения'''

    def point_is_inside(self, point: Point) -> bool:
        '''Проверяет входит ли точка во фрагмент'''
        if (
            point.x >= self.position.x and
            point.x <= self.position.x + self.width - 1 and
            point.y >= self.position.y and
            point.y <= self.position.y + self.height - 1
        ):
            return True
        else:
            return False

    def __init__(self):
        self.index: int
        self.position: Point
        self.width = 16
        self.height = 16
        self.black_count: int = 0
        self.is_white_outline: bool = False
        self.is_truncated: bool = False
        self.is_edge_image: bool = False