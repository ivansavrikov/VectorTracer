from PIL import Image
import math
from core.Fragment import Fragment
from core.Point import Point

#ВОЗМОЖЕН РЕФАКТОРИНГ
class ImagePreparer:

    def replace_transparent_background(image: Image):
        '''Заменяет прозрачный альфа канал на белый цвет'''
        background_color = 255
        new_image = Image.new('LA', image.size, background_color)
        mask = image.convert('LA')
        new_image.paste(image, (0, 0), mask)
        new_image = new_image.convert('L')
        return new_image

    def to_binary_image(image: Image):
        threshold = 100
        binary_image = image.point(lambda p: 0 if p < threshold else 255, '1')
        return binary_image

    def draw_fragments(image: Image) -> Image:
        square = Fragment()
        width_fragments: int = math.ceil(image.width/square.width) #ширина изображения в фрагментах
        height_fragments: int = math.ceil(image.height/square.height) #высота изображения в фрагментах

        for hf in range(height_fragments):
            for wf in range(width_fragments):

                fragment = Fragment()
                fragment.position = Point(wf*fragment.width, hf*fragment.height)

                for y in range(fragment.position.y, fragment.position.y + fragment.height):
                    for x in range(fragment.position.x, fragment.position.x + fragment.width):
                        point: Point = Point(x, y)
                        
                        width, height = image.size
                        if (0 <= point.x < width) and (0 <= point.y < height):
                            if (hf + wf) % 2 == 0:
                                image.putpixel((point.x, point.y), (0, 0, 0, 64))
        return image

    def prepare(image: Image) -> Image:
        '''Подготовливает изображение, для трассировки'''
        image = ImagePreparer.replace_transparent_background(image)
        image = ImagePreparer.to_binary_image(image)
        return image