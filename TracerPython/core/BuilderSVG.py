from PIL import Image
from core.ImageAnalyzer import ImageAnalyzer
from core.ImageData import ImageData
from core.ImagePreparer import ImagePreparer
from core.Pointer import Pointer
from core.Point import Point

class BuilderSVG:

    def svg_open(self, width: int, height: int):
        self.svg_code = f'''<svg
    width="{width}" height="{height}" 
    viewBox="0 0 {width} {height}" 
    xmlns="http://www.w3.org/2000/svg">'''

    def add_move(self, point: Point):
        self.path_data += f'M {point.x} {point.y} '

    def add_line(self, point: Point):
        self.path_data += f'L {point.x} {point.y} '

    def add_path(self):
        self.svg_code += f'\n\t<path fill="none" stroke="black" stroke-width="2" stroke-linejoin="round" \n\t\td="{self.path_data}Z"/> \n'
        self.path_data = ''

    def add_circle(self, center: Point, radius=5):
        self.svg_code += f'''\n\t<circle cx="{center.x}" cy="{center.y}" r="{radius}" stroke="black" stroke-width="1" fill="red" />'''

    def svg_close(self):
        self.svg_code += '\n</svg>'

    def trace(self, image: Image):
        image = ImagePreparer.prepare(image)
        data: ImageData = ImageAnalyzer.analyze(image)
        pointer: Pointer = Pointer(image)

        width, height = image.size
        self.svg_open(width, height)

        smooth_range_x = width / 100
        smooth_range_y = height / 100

        for fragment in data.fragments:
            pointer.calculate_start_position(fragment.position)

            first = pointer.pos
            corner = first

            self.add_circle(first) #for debug
            self.add_move(first)

            i = 1
            corners_count = 0
            while True:
                prev = pointer.pos
                pointer.perform_move()

                for fragment in data.fragments:
                    if (
                        pointer.pos.x >= fragment.position.x and
                        pointer.pos.x <= fragment.position.x + fragment.width and
                        pointer.pos.y >= fragment.position.y and
                        pointer.pos.y <= fragment.position.y + fragment.height
                    ):
                        data.fragments.remove(fragment)

                if pointer.arrow_is_changed:
                    potential = prev
                    
                    if (abs(potential.x - corner.x) >= smooth_range_x or abs(potential.y - corner.y) >= smooth_range_y):
                        corner = potential

                        self.add_line(corner)
                        
                        corners_count += 1                      
                        if corners_count % 10 == 0:
                            self.path_data += '\n\t\t'
                            
                    if potential == first:
                        break
                    i += 1
            
            self.add_path()
        self.svg_close()
        return self.svg_code

    def __init__(self):
        self.path_data: str = ''
        self.svg_code: str = ''