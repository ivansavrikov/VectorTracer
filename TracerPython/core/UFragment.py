from core.Point import Point



class UFragment:
    '''Данные Квадратного фрагмента изображения'''

    size: int = 10

    def point_is_inside(self, point: Point) -> bool:
        '''Проверяет входит ли точка во фрагмент'''
        if (
            point.x >= self.position.x and
            point.x <= self.position.x + UFragment.size - 1 and
            point.y >= self.position.y and
            point.y <= self.position.y + UFragment.size - 1
        ):
            return True
        else:
            return False

    def __init__(self):
        self.index = 0
        self.position: Point

        self.colors: dict = dict()

        self.is_truncated: bool = False