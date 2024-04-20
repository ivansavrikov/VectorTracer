from PIL import Image
from core.UFragment import UFragment
from core.Point import Point
from core.UPointer import UPointer
from typing import List
import math

class UAnalyzer:

    def analyze(image: Image) -> list[UFragment]:
        fragments: List[UFragment] = []

        width_fragments: int = math.ceil(image.width/UFragment.size) #ширина изображения в фрагментах
        height_fragments: int = math.ceil(image.height/UFragment.size) #высота изображения в фрагментах

        pointer: UPointer = UPointer(image)

        for hf in range(height_fragments):
            for wf in range(width_fragments):
                fragment = UFragment()
                fragment.position = Point(wf*UFragment.size, hf*UFragment.size)
                
                for y in range(fragment.position.y, fragment.position.y + UFragment.size):
                    for x in range(fragment.position.x, fragment.position.x + UFragment.size):
                        point: Point = Point(x, y)
                        if pointer.pixel_is_inside_image(point): #Пиксель в пределах изображения
                            r, g, b = image.getpixel((point.x, point.y))
                            color = f"{r},{g},{b}"
                            if color not in fragment.colors:
                                fragment.colors[color] = 1
                            else:
                                fragment.colors[color] += 1
                
                if len(fragment.colors.keys()) > 1:
                    fragment.colors = sorted(fragment.colors.items(), key=lambda x: x[1])
                    fragment.colors = reversed(fragment.colors)
                    fragment.colors = dict(fragment.colors)
                    fragments.append(fragment)

        return fragments