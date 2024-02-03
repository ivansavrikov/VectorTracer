from PIL import Image
from core.Fragment import Fragment
from core.ImagePreparer import ImagePreparer 
from core.Point import Point
from core.Pointer import Pointer
from core.ImageData import ImageData
import math

class ImageAnalyzer:

    def analyze(image: Image) -> ImageData:
        image_data: ImageData = ImageData(image)
        image = ImagePreparer.prepare(image)
        pointer: Pointer = Pointer(image)

        square = Fragment()
        width_fragments: int = math.ceil(image.width/square.width) #ширина изображения в фрагментах
        height_fragments: int = math.ceil(image.height/square.height) #высота изображения в фрагментах
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
                        else:
                            fragment.is_truncated = True
                
                # угловые точки фрагмента с отступом 1
                outside_point1 = Point(fragment.position.x-1, fragment.position.y-1)
                outside_point2 = Point(fragment.position.x-1, fragment.position.y+fragment.height)
                outside_point3 = Point(fragment.position.x+fragment.width, fragment.position.y-1)
                outside_point4 = Point(fragment.position.x+fragment.width, fragment.position.y+fragment.height)

                if (not pointer.pixel_is_inside_image(outside_point1) 
                    or not pointer.pixel_is_inside_image(outside_point2) 
                    or not pointer.pixel_is_inside_image(outside_point3) 
                    or not pointer.pixel_is_inside_image(outside_point4)):
                        fragment.is_edge_image = True
                
                width, height = fragment.width, fragment.height
                fragment_area = width*height
                if fragment.is_truncated:
                    t_width = image.width - fragment.position.x
                    t_height = image.height - fragment.position.y
                    if t_width < width:
                        width = t_width
                    if t_height < height:
                        height = t_height
                    fragment_area = width*height

                is_shape_edge = False
                if fragment.black_count == fragment_area:
                    if pointer.pixel_is_possible(outside_point1, 255):
                        fragment.position = outside_point1
                        is_shape_edge = True
                        fragment.is_white_outline = False
                    if fragment.is_edge_image and not pointer.pixel_is_inside_image(outside_point1):
                        is_shape_edge = True
                        fragment.is_white_outline = False
                elif fragment.black_count > 0 and fragment.black_count < fragment_area:
                    is_shape_edge = True
                    if pointer.pixel_is_possible(fragment.position, 0):
                        fragment.is_white_outline = True

                if is_shape_edge:
                    image_data.fragments.append(fragment)
                    i += 1
                
        return image_data