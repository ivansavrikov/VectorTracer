import base64
from io import BytesIO, StringIO
from PIL import Image
from core.BuilderSVG import BuilderSVG as SVG
from core.Point import Point
from core.UPointer import UPointer
import math
from core.Console import Console as C
from core.DirectionEnum import Direction, ArrowSymbols
import time

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

	def vectorize(image: Image, smooth_range: int):
		svg_paths: StringIO = StringIO()
		svg_paths.write(SVG.paths_group_open())
		pointer = UPointer(image)
		width, height = image.size

		start_points = []
		svg_points_count = 0
		path_index = 0
		for y in range(height):
			for x in range(width):
				if not pointer.pixels[x, y]: continue
				start_position = Point(x, y)
				closing_position = start_position
				pointer.color = pointer.get_color(start_position)

				# if pointer.pixel_is_contour(start_position):
				if pointer.pixel_is_strict_contour(start_position):
					pointer.set_start_position(start_position)

					path_data = []
					path_data.append(SVG.move_to(start_position))
					path_points = []
					path_points.append(start_position)
					prev_corner = start_position
					path_points_count = 1

					positions_to_block = []
					positions_to_block.append((start_position.x, start_position.y))

					positions_arrows = []
					# positions_arrows.append(SVG.add_fragment(pointer.pos, 1, 1, stroke=SVG.get_hex_code(*pointer.color)))
					# positions_arrows.append(SVG.add_text(Point(pointer.pos.x-0.15, pointer.pos.y+0.15), ArrowSymbols.ARROWS[pointer.arrow.value], color='red'))

					is_error_path = False
					i = 0
					while True:
						prev_position = pointer.pos
						possible_position, possible_arrow = pointer.calc_possible_position(pointer.arrow)

						if i >= 1_000_000 or path_points_count >= 100_000:
							is_error_path = True
							print(f'infinity exception: path={path_index} loops={i} path_points={path_points_count} st1={start_position} st2={closing_position} color={pointer.color}')
							# raise Exception(f"error path {path_index}")
							break

						is_replace_closing_position = False
						recalc_arrow = possible_arrow
						while True: #TODO: возможно можно упростить
							if possible_position.x != pointer.pos.x and possible_position.y != pointer.pos.y:
								t1 = Point(possible_position.x, pointer.pos.y)
								t2 = Point(pointer.pos.x, possible_position.y)
								if pointer.get_color(t1) == pointer.get_color(t2) and pointer.get_color(pointer.pos) != pointer.get_color(t1):
									if recalc_arrow.value % 90 != 0: recalc_arrow = pointer.arrow_from_degrees(recalc_arrow.value + 45)
									recalc_arrow = pointer.calc_arrow(recalc_arrow)
									possible_position, recalc_arrow = pointer.calc_possible_position(recalc_arrow)
									if recalc_arrow == possible_arrow:
										is_replace_closing_position = True
										break
								else: break
							else: break

						if pointer.position_is_available(possible_position):
							pointer.pos = possible_position
							pointer.moves_count += 1
							# positions_arrows.append(SVG.add_fragment(pointer.pos, 1, 1, stroke=SVG.get_hex_code(*pointer.color)))
							# positions_arrows.append(SVG.add_text(Point(pointer.pos.x-0.15, pointer.pos.y+0.15), ArrowSymbols.ARROWS[pointer.arrow.value], color=SVG.get_hex_code(*pointer.color)))
							positions_to_block.append((pointer.pos.x, pointer.pos.y))
							pointer.rotate_arrow(recalc_arrow)

							if pointer.arrow_is_changed and prev_position != start_position:
								if (
									abs(prev_position.x - prev_corner.x) >= smooth_range or
									abs(prev_position.y - prev_corner.y) >= smooth_range
								):
									# path_data.append(SVG.line_to(prev_position))
									path_points.append(prev_position)
									
									if (len(path_points)-1) % 3 == 0 and len(path_points) >= 4:
										angle_between_1_3 = UTracer.calc_angle(path_points[-4], path_points[-3], path_points[-2])
										angle_between_2_4 = UTracer.calc_angle(path_points[-3], path_points[-2], path_points[-1])
										if angle_between_1_3 != 90 and angle_between_2_4 != 90:
											p0, c1, c2, p1 = UTracer.get_curve_points(path_points[-4], path_points[-3], path_points[-2], path_points[-1])
											path_data.append(SVG.curve_to(p0, c1, c2, p1))
										elif angle_between_1_3 == 90 or angle_between_2_4 == 90:
											for index in range(4, 0, -1):
												path_data.append(SVG.line_to(path_points[-index]))

									path_points_count += 1
									if path_points_count % 10 == 0:
										path_data.append('\n\t\t\t\t')
									prev_corner = prev_position

							if pointer.pos == start_position:
								break
							
							if pointer.pos == closing_position:
								path_data.append(SVG.line_to(pointer.pos))
								# path_points.append(pointer.pos)
								path_points_count += 1
								break
							if is_replace_closing_position:
								closing_position = pointer.pos
				
						else:
							is_error_path = True
							# path_data.append(SVG.line_to(pointer.pos))
							path_points.append(pointer.pos)
							path_points_count += 1
							raise Exception(f"error path {path_index}")

						i += 1
					
					for p in positions_to_block:
						xp, yp = p
						pointer.pixels[xp, yp] = False

					if path_points_count >= 3:

						remains = len(path_points) % 3
						if remains == 1:
							path_data.append(SVG.line_to(path_points[0]))
						if remains == 2:
							c1 = UTracer.calc_control_point(path_points[-2], path_points[-1], path_points[0])
							path_data.append(SVG.add_quadratic_bezier(path_points[-2], c1, path_points[0]))
						remains = len(path_points) % 3
						if remains == 0: #FIXME: не учитывается 90 угол
							p0, c1, c2, p1 = UTracer.get_curve_points(path_points[-3], path_points[-2], path_points[-1], path_points[0])
							path_data.append(SVG.curve_to(p0, c1, c2, p1))

						hex = SVG.get_hex_code(*pointer.color)
						# svg_paths.write(SVG.path_open(path_index, fill='none', stroke='red'))		
						svg_paths.write(SVG.path_open(path_index, fill=hex, stroke=hex))
						svg_paths.write("".join(path_data))
						if is_error_path: 
							start_points.append(SVG.add_circle(closing_position, radius=0.5, fill='green', stroke='red', stroke_width=0.05))
							start_points.append(SVG.add_text(Point(closing_position.x-0.15, closing_position.y+0.15), path_index, color='darkred'))
						
						svg_paths.write(SVG.path_close(is_closed=not is_error_path))
						# svg_paths.write("".join(positions_arrows))
						start_points.append(SVG.add_circle(start_position, radius=0.5, fill=hex, stroke='red', stroke_width=0.05))
						start_points.append(SVG.add_text(Point(start_position.x-0.15, start_position.y+0.15), path_index, color='darkred'))

					path_index += 1
					svg_points_count += len(path_data)
		
		svg_paths.write(SVG.group_close())
		paths = svg_paths.getvalue()
		svg_paths.close()
		# paths += ''.join(start_points)
		print(f'getting pixels = {pointer.getting_pixels_count:_}\npointer set position count = {pointer.moves_count:_}\ncalced points count={svg_points_count:_}\nratio pxs/getpxs = {(pointer.getting_pixels_count/(image.width*image.height)):.2f}')
		return paths

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