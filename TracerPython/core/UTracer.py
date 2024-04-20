from PIL import Image
from core.BuilderSVG import BuilderSVG
from core.Point import Point
from core.UPointer import UPointer
import math
from core.UAnalyzer import UAnalyzer
from core.UFragment import UFragment
from core.Exceptions import MyCustomException

class UTracer:

    def trace(image: Image, draw_fragments=False):
    
        svg = BuilderSVG()
        image = image.convert("RGB")
        fragments = UAnalyzer.analyze(image)
        print(f"Фрагментов {len(fragments)}")

        for f in fragments:
            if '255,255,255' in f.colors:
                del f.colors["255,255,255"]

        pointer: UPointer = UPointer(image)

        width, height = image.size
        svg.svg_open(width, height)

        svg.open_group()

        # 5 - normal   
        smooth_range_x = 1
        smooth_range_y = 1

        while len(fragments) > 0:
            fragment = fragments[0]

            for color in list(fragment.colors.keys()):
                r, g, b = color.split(',')
                pointer.color = (int(r), int(g), int(b))
                pointer.calculate_start_position(fragment.position, Point(fragment.position.x + UFragment.size-1, fragment.position.y + UFragment.size-1))

                first = pointer.pos
                corner = first

                svg.add_move(first)

                corners_count = 1
                while True:
                    prev = pointer.pos

                    for f in fragments:
                        if f.point_is_inside(pointer.pos):
                            if color in f.colors: del f.colors[color]
                            if len(f.colors) == 0: fragments.remove(f)
                            break

                    try:
                        pointer.perform_move()
                    except MyCustomException:
                        print(f'Исключение: {pointer.pos.x} {pointer.pos.y}')
                        break
                    
                    if pointer.arrow_is_changed:
                        # print(pointer.arrow.value)
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
            
                hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
                svg.add_path(hex, stroke=hex)
        
        svg.close_group()

        
        if draw_fragments:
            svg.open_group()
            fragments = UAnalyzer.analyze(image)
            for fragment in fragments:
                svg.add_rectangle(fragment.position, UFragment.size, UFragment.size, fill='none')
                # svg.add_text(Point(fragment.position.x, UFragment.size.y+UFragment.size/2), f'')
            svg.close_group()

        svg.svg_close()
        return svg.svg_code