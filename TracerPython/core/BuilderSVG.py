from PIL import Image
from core.Pointer import Pointer
from core.Point import Point

class BuilderSVG:

    def add_curve(self, point: Point):
        self.path_data += f' {point.x} {point.y}, '

    def add_line(self, point: Point):
        self.path_data += f'L {point.x} {point.y} '

    def raster_to_svg(self, image: Image) -> str:
        width, height = image.size
        pointer = Pointer(image)
        
        # smooth_range = 12
        smooth_range_x = width / 100
        smooth_range_y = height / 100
        first = pointer.pos
        corner = first
        i = 1
        corners_count = 0
        while True:
            prev = pointer.pos
            pointer.perform_move()
            if pointer.arrow_is_changed:
                potential = prev
                if abs(potential.x - corner.x) >= smooth_range_x or abs(potential.y - corner.y) >= smooth_range_y:
                    corner = potential
                    # self.add_curve(corner)
                    self.add_line(corner)
                    corners_count += 1
                    
                    if corners_count % 10 == 0:
                        self.path_data += '\n\t\t\t'
                        
                if potential == first:
                    break

                i += 1

        print(f"Углов у фигуры {corners_count}")
        print(f'Всего движений {pointer.moves_count}')

        line_or_curve = '' #Line
        # line_or_curve = ' C ' #Curve
        
        scale = 2
        svg_code = f"""<svg width="{width*scale}" height="{height*scale}" viewBox="0 0 {width*scale} {height*scale}" xmlns="http://www.w3.org/2000/svg">
        <g transform="scale({scale})">
            <path d="\n\t\t\tM {first.x} {first.y} {line_or_curve}{self.path_data}Z"\n\t\t\tfill="black" stroke="none" stroke-width="1" stroke-linejoin="round"/>
        </g>
    </svg>"""
        return svg_code
    
    
    def __init__(self):
        self.path_data: str = ""