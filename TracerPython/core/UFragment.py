from core.Point import Point



class UFragment:
    '''Данные Квадратного фрагмента изображения'''

    size: int = 16

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
        self.position: Point

        self.colors: dict = dict()

        self.is_truncated: bool = False