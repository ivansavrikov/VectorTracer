import base64
from io import BytesIO, StringIO
from PIL import Image
from core.BuilderSVG import BuilderSVG as SVG
from core.Point import Point
from core.UPointer import UPointer
import math
from core.Console import Console as C
from core.Directions import Directions, ArrowSymbols, rotate_clockwise
from core.SquareAnalyzer import optimaze
import time
from enum import Enum

class UTracer:
	def calc_angle(p1, p2, p3):
		v1 = p1 - p2
		v2 = p3 - p2
		cos = (v1.x*v2.x + v1.y*v2.y)/(v1.length()*v2.length())
		cos = max(-1, min(1, cos))
		acos = math.acos(cos)
		return int(math.degrees(acos))

	def calc_control_point(p1, p2, p3, tension=2.0):
		v1 = p1 - p2
		v2 = p3 - p2
		bisector_point = (p1 * v2.length() + p3 * v1.length())/(v1.length()+v2.length())
		control = bisector_point*(1-tension)+p2*tension
		return control.round(decimals=1)

	def get_curve_points(p1: Point, p2: Point, p3: Point, p4: Point, tension=2.0):
		c1 = UTracer.calc_control_point(p1, p2, p3)
		c2 = UTracer.calc_control_point(p2, p3, p4)
		return p1, c1, c2, p4

	def trace(image: Image, detailing: int, mode: int):
		svg_paths: StringIO = StringIO()
		if mode == 1:
			svg_paths.write(SVG.paths_group_open(stroke_line_join='mitter'))
		elif mode == 2:
			svg_paths.write(SVG.paths_group_open(stroke_line_join='round'))
		pointer = UPointer(image)

		start_time = time.time()
		optimaze(image, pointer.available_positions)
		end_time = time.time()
		print(f"Optimize time = {(end_time-start_time):.2f} sec")

		width, height = image.size
		path_index = 0
		for y in range(height):
			for x in range(width):
				if not pointer.available_positions[x, y]: continue
				start_position = Point(x, y)
				closing_position = start_position
				pointer.current_color = pointer.get_color(start_position)

				if pointer.pixel_is_contour(start_position):
					pointer.set_start_position(start_position)

					path_data = []
					path_points = []
					positions_to_block = []

					path_data.append(SVG.move_to(start_position))
					path_points.append(start_position)
					positions_to_block.append((start_position.x, start_position.y))

					prev_corner = start_position

					while True:
						prev_position = pointer.position
						possible_position, possible_direction = pointer.calc_possible_position(pointer.direction)
						is_update_closing_position = False
						recalced_direction = possible_direction

						while True:
							if possible_position.x != pointer.position.x and possible_position.y != pointer.position.y:
								px1_color = pointer.get_color(Point(possible_position.x, pointer.position.y))
								px2_color =  pointer.get_color(Point(pointer.position.x, possible_position.y))
								if px1_color == px2_color and pointer.current_color != px1_color:
									if recalced_direction.value % 2 != 0: recalced_direction = rotate_clockwise(recalced_direction, 1)
									recalced_direction = pointer.calc_direction(recalced_direction)
									possible_position, recalced_direction = pointer.calc_possible_position(recalced_direction)
									if recalced_direction == possible_direction:
										is_update_closing_position = True
										break
								else: break
							else: break

						pointer.position = possible_position
						pointer.rotate_direction(recalced_direction)
						positions_to_block.append((pointer.position.x, pointer.position.y))
						
						if pointer.direction_is_changed and prev_position != start_position:
							if (
								abs(prev_position.x - prev_corner.x) >= detailing or
								abs(prev_position.y - prev_corner.y) >= detailing
							):
								path_points.append(prev_position)
								prev_corner = prev_position

								if mode == 1:
									path_data.append(SVG.line_to(prev_position))

								if mode == 2:
									if (len(path_points)-1) % 3 == 0 and len(path_points) >= 4:
										angle_between_1_3 = UTracer.calc_angle(path_points[-4], path_points[-3], path_points[-2])
										angle_between_2_4 = UTracer.calc_angle(path_points[-3], path_points[-2], path_points[-1])
										if angle_between_1_3 != 90 and angle_between_2_4 != 90:
											p0, c1, c2, p1 = UTracer.get_curve_points(path_points[-4], path_points[-3], path_points[-2], path_points[-1])
											path_data.append(SVG.curve_to(p0, c1, c2, p1))
										elif angle_between_1_3 == 90 or angle_between_2_4 == 90:
											for index in range(4, 0, -1):
												path_data.append(SVG.line_to(path_points[-index]))

								if len(path_points) % 10 == 0:
									path_data.append(f'\n{'\t'*4}')
								
						if pointer.position == start_position:
							break
						if pointer.position == closing_position:
							path_points.append(pointer.position)
							break
						if is_update_closing_position:
							closing_position = pointer.position
					
					for p in positions_to_block:
						xp, yp = p
						pointer.available_positions[xp, yp] = False

					if len(path_points) >= 2:
						hex = SVG.get_hex_code(*pointer.current_color)

						if len(path_points) == 1:
							svg_paths.write(SVG.add_circle(path_points[0], radius=0.8, fill=hex, stroke=hex, stroke_width=0) + '\n')
							continue

						if mode == 2:
							remains = len(path_points) % 3
							if remains == 1:
								path_data.append(SVG.line_to(path_points[-1]))
							if remains == 2:
								c1 = UTracer.calc_control_point(path_points[-2], path_points[-1], path_points[0])
								path_data.append(SVG.add_quadratic_bezier(path_points[-2], c1, path_points[0]))
							remains = len(path_points) % 3
							if remains == 0:
								p0, c1, c2, p1 = UTracer.get_curve_points(path_points[-3], path_points[-2], path_points[-1], path_points[0])
								path_data.append(SVG.curve_to(p0, c1, c2, p1))

						svg_paths.write(SVG.path_open(path_index, fill=hex, stroke=hex))
						svg_paths.write("".join(path_data))
						svg_paths.write(SVG.path_close(True))

					path_index += 1
		
		svg_paths.write(SVG.group_close())
		svg_shapes = svg_paths.getvalue()
		svg_paths.close()
		return svg_shapes

	def put_image(image: Image, pos=Point(0,0)):
		svg_image: StringIO = StringIO()
		
		image_bytes_io = BytesIO()
		image.save(image_bytes_io, format="PNG")
		image_bytes = image_bytes_io.getvalue()
		image_data = base64.b64encode(image_bytes).decode('utf-8')

		svg_image.write(SVG.add_image(image_data, image.width, image.height, pos))

		result = svg_image.getvalue()
		svg_image.close()
		return result