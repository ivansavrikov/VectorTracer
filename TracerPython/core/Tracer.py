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
    def calc_controll_point(start, end, distance, reverse=False):
        # Находим середину отрезка
        midpoint = Point((start.x + end.x) / 2, (start.y + end.y) / 2)

        # Находим вектор от начальной точки к середине
        vector_AB = Point(midpoint.x - start.x, midpoint.y - start.y)

        # Поворачиваем вектор на 90 градусов (по часовой стрелке)
        vector_perpendicular = Point(-vector_AB.y, vector_AB.x)

        # Нормализуем вектор (приводим к длине 1)
        length = math.sqrt(vector_perpendicular.x ** 2 + vector_perpendicular.y ** 2)
        normalized_vector = Point(vector_perpendicular.x / length, vector_perpendicular.y / length)

        # Умножаем нормализованный вектор на заданное расстояние
        # scaled_vector = Point(normalized_vector.x * distance, normalized_vector.y * distance)
        distance = math.sqrt(vector_perpendicular.x ** 2 + vector_perpendicular.y ** 2)
        scaled_vector = Point((vector_perpendicular.x / distance) * (distance / 2), (vector_perpendicular.y / distance) * (distance / 2))

        # Находим координаты точки над серединой отрезка
        if not reverse:
            controll_point = Point(midpoint.x - scaled_vector.x, midpoint.y - scaled_vector.y)
        elif reverse:
            controll_point = Point(midpoint.x + scaled_vector.x, midpoint.y + scaled_vector.y)

        controll_point.x = round(controll_point.x, 1)
        controll_point.y = round(controll_point.y, 1)
        return controll_point

    def trace(image: Image, draw_fragments: bool=False):
        svg = BuilderSVG()
        image = ImagePreparer.prepare(image)
        data: ImageData = ImageAnalyzer.analyze(image)
        pointer: Pointer = Pointer(image)

        width, height = image.size
        svg.svg_open(width, height)
        svg.open_group()

        smooth_range_x = width / 120
        smooth_range_y = height / 120

        # smooth_range_x = 1
        # smooth_range_y = 1

        general_path_data: str = ''
        while True:
            if len(data.fragments) == 0:
                break
            fragment = data.fragments[0]
            data.fragments.remove(fragment)
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

                if pointer.pos == first:
                    svg.add_line(first)
                    break

                if pointer.pos == Point(0, 0):
                    path_contain_zero_point = True

                for f in data.fragments:
                    if f.point_is_inside(pointer.pos):
                        data.fragments.remove(f)
                        # if fragment.is_edge_image:
                        #     if f.is_edge_image:
                        #         data.fragments.remove(f)
                        # else:
                        #     data.fragments.remove(f)
                        break

                if pointer.arrow_is_changed:
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
            
            # fill_color = 'black'
            # if pointer.trace_color == 255:
            #     fill_color = 'white'
            
            # if corners_count >= 3 and not path_contain_zero_point:
            #     if fill_color == 'black':
            #         svg.add_path(fill_color, stroke='none')
            #     elif fill_color == 'white':
            #         svg.add_path('white', stroke='none', opacity='1')
            # else:
            #     svg.path_data = ''

            svg.path_data += 'Z'
            if corners_count >= 3 and not path_contain_zero_point:
                general_path_data += svg.path_data
            svg.path_data = ''
        
        svg.path_data = ''
        svg.path_data += general_path_data
        svg.add_path('black', stroke='none')
        svg.close_group()

        if draw_fragments:
            data: ImageData = ImageAnalyzer.analyze(image)
            for fragment in data.fragments:
                if fragment.is_white_outline:
                    svg.add_rectangle(fragment.position, fragment.width, fragment.height, fill='red')
                    svg.add_text(Point(fragment.position.x, fragment.position.y+fragment.height/2), fragment.index)
                else:
                    svg.add_rectangle(fragment.position, fragment.width, fragment.height, fill='none')
                    svg.add_text(Point(fragment.position.x, fragment.position.y+fragment.height/2), fragment.index)

                
        svg.svg_close()
        return svg.svg_code