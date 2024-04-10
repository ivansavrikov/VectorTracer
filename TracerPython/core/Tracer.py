import base64
from io import BytesIO
from PIL import Image
from core.BuilderSVG import BuilderSVG
from core.Point import Point
from core.Pointer import Pointer
from core.ImagePreparer import ImagePreparer
from core.ImageData import ImageData
from core.ImageAnalyzer import ImageAnalyzer
from core.LimitedList import LimitedList
import math

class Tracer:

    def trace(image: Image, draw_fragments: bool=False):
    
        svg = BuilderSVG()
        image = ImagePreparer.prepare(image)
        data: ImageData = ImageAnalyzer.analyze(image)
        pointer: Pointer = Pointer(image)

        width, height = image.size
        svg.svg_open(width, height)

        #temp
        # image_bytes_io = BytesIO()
        # image.save(image_bytes_io, format="PNG")
        # image_bytes = image_bytes_io.getvalue()
        # image_data = base64.b64encode(image_bytes).decode('utf-8')
        # svg.add_image(image_data, image.width, image.height)

        svg.open_group()

        # smooth_range_x = width / 120
        # smooth_range_y = height / 120

        # 5 - normal   
        smooth_range_x = 1
        smooth_range_y = 1

        starting_fragments = []
        general_path_data: str = ''
        while True:
            if len(data.fragments) == 0:
                break
            fragment = data.fragments[0]
            starting_fragments.append(fragment)
            # print(f"fragment {fragment.index}, is_white = {fragment.is_white_outline}")

            pointer.calculate_start_position(fragment.position, Point(fragment.position.x + fragment.width-1, fragment.position.y + fragment.height-1), is_white=fragment.is_white_outline)

            first = pointer.pos
            corner = first

            # last_2_points = LimitedList(max_length=2)
            svg.add_move(first)
            # last_2_points.add(first)
            path_contain_zero_point = False

            corners_count = 1
            while True:
                prev = pointer.pos
                pointer.perform_move()

                if pointer.pos == Point(0, 0):
                    path_contain_zero_point = True

                for f in data.fragments:
                    if f.point_is_inside(pointer.pos):
                        data.fragments.remove(f)
                        break
                
                if pointer.arrow_is_changed:
                    print(pointer.arrow.value)
                    potential = prev
                    if (abs(potential.x - corner.x) >= smooth_range_x or 
                        abs(potential.y - corner.y) >= smooth_range_y):
                        corner = potential
                        svg.add_line(corner)

                        # last_2_points.add(corner)
                        # if len(last_2_points.get_all()) == 2:
                        #     start: Point = last_2_points.get(0)
                        #     end: Point = last_2_points.get(1)
                        #     if corners_count % 2 == 0:
                        #         controll: Point = Tracer.calc_controll_point(start, end, 2, reverse=False)
                        #     else:
                        #         controll: Point = Tracer.calc_controll_point(start, end, 2, reverse=True)
                            
                        #     svg.add_quadratic_bezier(controll, end)

                        corners_count += 1                      
                        if corners_count % 10 == 0:
                            svg.path_data += '\n\t\t'                    

                if pointer.pos == first:
                    break
            fill_color = 'black'
            if pointer.trace_color == 255:
                fill_color = 'white'
            
            if corners_count >= 3 and not path_contain_zero_point:
                if fill_color == 'black':
                    svg.add_path('black', stroke='none', opacity='1')
                elif fill_color == 'white':
                    svg.add_path('white', stroke='none', opacity='1')
            else:
                svg.path_data = ''

            # svg.path_data += 'Z'
            # if corners_count >= 3 and not path_contain_zero_point:
            #     general_path_data += svg.path_data
            # svg.path_data = ''
        
        svg.path_data = ''
        svg.path_data += general_path_data
        svg.add_path('black', stroke='none')
        svg.close_group()

        if draw_fragments:
            data: ImageData = ImageAnalyzer.analyze(image)
            for fragment in data.fragments:
                if fragment.is_white_outline:
                    svg.add_rectangle(fragment.position, fragment.width, fragment.height, fill='red')
                    svg.add_text(Point(fragment.position.x, fragment.position.y+fragment.height/2), f'{fragment.index}б')
                else:
                    svg.add_rectangle(fragment.position, fragment.width, fragment.height, fill='none')
                    svg.add_text(Point(fragment.position.x, fragment.position.y+fragment.height/2), f'{fragment.index}ч')

        # if draw_fragments:
        #     for f in starting_fragments:
        #         if f.is_white_outline:
        #             svg.add_rectangle(f.position, f.width, f.height, fill='white')
        #             svg.add_text(Point(f.position.x, f.position.y+f.height/2), f'{f.index}')
        #         else:
        #             svg.add_rectangle(f.position, f.width, f.height, fill='none')
        #             svg.add_text(Point(f.position.x, f.position.y+f.height/2), f'{f.index}')
                
        svg.svg_close()
        return svg.svg_code