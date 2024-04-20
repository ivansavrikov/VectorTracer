from PIL import Image
from core.BuilderSVG import BuilderSVG
from core.Point import Point
from core.UPointer import UPointer
import math
from core.UAnalyzer import UAnalyzer
from core.UFragment import UFragment

class UTracer:

    def trace(image: Image):
    
        svg = BuilderSVG()
        fragments = UAnalyzer.analyze(image)
        pointer: UPointer = UPointer(image)

        width, height = image.size
        svg.svg_open(width, height)

        svg.open_group()

        # 5 - normal   
        smooth_range_x = 1
        smooth_range_y = 1

        general_path_data: str = ''
        while len(fragments) > 0:
            fragment = fragments[0]

            color = fragment.colors.keys()[0]
            r, g, b = color.split(',')
            pointer.color = (int(r), int(g), int(b))
            pointer.calculate_start_position(fragment.position, Point(fragment.position.x + UFragment.size-1, fragment.position.y + UFragment.size-1))

            first = pointer.pos
            corner = first

            svg.add_move(first)

            corners_count = 1
            while True:
                prev = pointer.pos
                pointer.perform_move()

                for f in fragments:
                    if f.point_is_inside(pointer.pos):
                        fragments.remove(f)
                        break
                
                if pointer.arrow_is_changed:
                    print(pointer.arrow.value)
                    potential = prev
                    if (abs(potential.x - corner.x) >= smooth_range_x or 
                        abs(potential.y - corner.y) >= smooth_range_y):
                        corner = potential
                        svg.add_line(corner)

                        corners_count += 1                      
                        if corners_count % 10 == 0:
                            svg.path_data += '\n\t\t'                    

                if pointer.pos == first:
                    break
        
            svg.add_path('#{:02x}{:02x}{:02x}'.format(*pointer.color), stroke='none')
        
        svg.close_group()
        svg.svg_close()
        return svg.svg_code