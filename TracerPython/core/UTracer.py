import base64
from io import BytesIO
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
        print(f"\nFragments: {len(fragments)}")

        for f in fragments:
            for c in list(f.colors):
                r, g, b = c.split(',')
                if int(r) > 200 and int(g) > 200 and int(b) > 200: del f.colors[c]
            # if '255,255,255' in f.colors:
            #     del f.colors["255,255,255"]

        pointer: UPointer = UPointer(image)

        width, height = image.size
        svg.svg_open(width, height)

        # #temp
        # image_bytes_io = BytesIO()
        # image.save(image_bytes_io, format="PNG")
        # image_bytes = image_bytes_io.getvalue()
        # image_data = base64.b64encode(image_bytes).decode('utf-8')
        # svg.add_image(image_data, image.width, image.height)
        
        # if draw_fragments:
        #     svg.open_group()
        #     fragments = UAnalyzer.analyze(image)
        #     for fragment in fragments:
        #         svg.add_rectangle(fragment.position, UFragment.size, UFragment.size, fill='none')
        #         svg.add_text(Point(fragment.position.x, fragment.position.y+UFragment.size/2), f'{fragment.index}')
        #     svg.close_group()

        # svg.svg_close()
        # return svg.svg_code
    
        svg.open_group()

        # 5 - normal   
        smooth_range_x = 5
        smooth_range_y = 5

        start_fragments = []
        is_break = False
        while len(fragments) > 0:
            if is_break: break
            fragment = fragments[0]
            start_fragments.append(fragment)
            for color in list(fragment.colors.keys()):
                r, g, b = color.split(',')
                pointer.color = (int(r), int(g), int(b))
                pointer.calculate_start_position(fragment.position, Point(fragment.position.x + UFragment.size-1, fragment.position.y + UFragment.size-1))

                first = pointer.pos
                first_arrow = pointer.arrow
                corner = first
                # print(f'\nfragment index = {fragment.index}\ncolor = {color}\nstart_pos = {first.x} {first.y}\narrow = {first_arrow.value}\n')

                svg.add_move(first)

                corners_count = 1
                while True:
                    # if corners_count >= 10000:
                    #     is_break = True
                    #     print(f'ошибка в контуре 10000 \nstart_pos {first.x} {first.y}\nstart_arrow {first_arrow}\ntrace_color = {pointer.color}')
                    #     hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
                    #     svg.add_path('none', stroke='green')
                    #     svg.add_rectangle(fragment.position, UFragment.size, UFragment.size, fill='none')
                    #     svg.add_circle(first, 0.5)
                    #     break
                    prev = pointer.pos

                    for f in fragments:
                        if f.point_is_inside(pointer.pos):
                            if color in f.colors: del f.colors[color]
                            if len(f.colors) == 0: fragments.remove(f)
                            break

                    try:
                        pointer.perform_move()
                    except MyCustomException:
                        # print(f'Исключение: {pointer.pos.x} {pointer.pos.y}')
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
                                svg.path_data += '\n\t\t\t\t'                    

                    if pointer.pos == first:
                        break
            
                if corners_count > 5:
                    hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
                    svg.add_path(hex, stroke=hex)
                # svg.path_data = '' #test
        
        svg.close_group()

        
        if draw_fragments:
            svg.open_group()
            # fragments = UAnalyzer.analyze(image)
            for fragment in start_fragments:
                svg.add_rectangle(fragment.position, UFragment.size, UFragment.size, fill='none')
                svg.add_text(Point(fragment.position.x, fragment.position.y+UFragment.size/2), f'{fragment.index}')
            svg.close_group()

        svg.svg_close()
        print(f"Pointer position changes: {pointer.moves_count:,}")
        return svg.svg_code