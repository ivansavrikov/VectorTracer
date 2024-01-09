from PIL import Image
from core.Fragment import Fragment 
from core.Point import Point
from core.Pointer import Pointer
from core.ImageData import ImageData
import math


class ImageAnalyzer:

    def analyze(image: Image) -> ImageData:
        image_data: ImageData = ImageData(image)
        square = Fragment()
        width_fragments: int = math.ceil(image.width/square.width) #ширина изображения в фрагментах
        height_fragments: int = math.ceil(image.height/square.height) #высота изображения в фрагментах

        pointer: Pointer = Pointer(image)

        i: int = 0
        for hf in range(height_fragments):
            for wf in range(width_fragments):

                fragment = Fragment()
                fragment.index = i
                fragment.position = Point(wf*fragment.width, hf*fragment.height)

                for y in range(fragment.position.y, fragment.position.y + fragment.height):
                    for x in range(fragment.position.x, fragment.position.x + fragment.width):
                        point: Point = Point(x, y)
                        
                        if pointer.pixel_is_inside_image(point): #Пиксель в пределах изображения
                            if image.getpixel((point.x, point.y)) == 0:
                                fragment.black_count += 1
                
                if fragment.black_count == 0:
                    fragment.is_edge = False

                #иногда полностью черный фрагмент является краем фигуры (ВОЗМОЖНО ОПТИМИЗИРОВАТЬ)
                elif fragment.black_count == fragment.width*fragment.height:
                    pos: Point = Point(fragment.position.x-1, fragment.position.y-1)
                    for y in range(pos.y, pos.y + fragment.height+2):
                        for x in range(pos.x, pos.x + fragment.width+2):
                            point: Point = Point(x, y)
                            if pointer.pixel_is_inside_image(point):
                                if image.getpixel((point.x, point.y)) == 255:
                                    fragment.is_edge = True
                            else:
                                fragment.is_edge = True
                    
                elif fragment.black_count > 0 and fragment.black_count < fragment.width*fragment.height:
                    fragment.is_edge = True

                if fragment.is_edge == True:
                    image_data.fragments.append(fragment)
                
                i += 1
        return image_data


