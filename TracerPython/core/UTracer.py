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
	def calc_point(p1, p2, p3):
		v1 = p1 - p2
		v2 = p3 - p2
		X = (p1 * v2.length() + p3 * v1.length())/(v1.length()+v2.length())
		return X

	def bisector_vector(p1, p2, p3):
		v1 = p1 - p2
		v2 = p3 - p2

		# Нормализация векторов
		v1_normalized = v1.normalize()
		v2_normalized = v2.normalize()

		# Суммирование нормализованных векторов
		bisector = v1_normalized + v2_normalized

		# Нормализация результата
		bisector_normalized = bisector.normalize()

		return bisector_normalized

	def get_control_points(p1, p2, p3, p4, tension=2.0):
		# temp1 = (p3+p1)/2
		# temp1 = p2 + UTracer.bisector_vector(p1, p2, p3)
		temp1 = UTracer.calc_point(p1, p2, p3)

		c1 = temp1*(1-tension) + p2*tension
		# temp2 = (p4+p2)/2
		# temp2 = p3 + UTracer.bisector_vector(p2, p3, p4)
		temp2 = UTracer.calc_point(p2, p3, p4)

		c2 = temp2*(1-tension) + p3*tension
		return p1, c1.round(decimals=0), c2.round(decimals=0), p4

	def vectorize(image: Image):
		svg_paths: StringIO = StringIO()
		svg_paths.write(SVG.paths_group_open())
		pointer = UPointer(image)
		width, height = image.size

		start_points = []
		path_index = 0
		for y in range(height):
			for x in range(width):
				if not pointer.pixels[x, y]: continue
				start_position = Point(x, y)
				start_position_2 = Point(x, y)
				pointer.color = pointer.get_color(start_position)

				if pointer.pixel_is_possible(start_position) and pointer.pixel_is_contour(start_position):
					blocked_pixels = []
					blocked_pixels.append((x, y))
					
					pointer.pos = start_position
					pointer.arrow = pointer.calc_arrow()

					arrows = []

					path = []
					
					hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)

					path.append(SVG.move_to(start_position))
					path_points_count = 1
					i = 0
					while True:
						prev_position = pointer.pos
						possible_position, possible_arrow = pointer.calc_possible_position(pointer.arrow)

						if i >= 1_000_000 or path_points_count >= 100_000:
							hex = 'red'
							print(f'infinity exception: path={path_index} loops={i} path_points={path_points_count} st1={start_position} st2={start_position_2} color={pointer.color}')
							break

						start_is_offset = False
						recalc_arrow = possible_arrow
						while True:
							if possible_position.x != pointer.pos.x and possible_position.y != pointer.pos.y:
								t1 = Point(possible_position.x, pointer.pos.y)
								t2 = Point(pointer.pos.x, possible_position.y)
								if pointer.get_color(t1) == pointer.get_color(t2) and pointer.get_color(pointer.pos) != pointer.get_color(t1):
									if recalc_arrow.value % 90 != 0: recalc_arrow = pointer.arrow_from_degrees(recalc_arrow.value + 45)
									recalc_arrow = pointer.calc_arrow(recalc_arrow)
									possible_position, recalc_arrow = pointer.calc_possible_position(recalc_arrow)
									if recalc_arrow == possible_arrow:
										start_is_offset = True
										break
								else: break
							else: break

						if pointer.pixels[possible_position.x, possible_position.y]:
							pointer.pos = possible_position
							arrows.append(SVG.add_fragment(pointer.pos, 1, 1, stroke=hex))
							arrows.append(SVG.add_text(Point(pointer.pos.x-0.15, pointer.pos.y+0.15), ArrowSymbols.ARROWS[pointer.arrow.value], color=hex))
							blocked_pixels.append((pointer.pos.x, pointer.pos.y))
							pointer.rotate_arrow(recalc_arrow)

							if pointer.arrow_is_changed and prev_position != start_position:
								path.append(SVG.line_to(prev_position))
								path_points_count += 1
								if path_points_count % 10 == 0:
									path.append('\n\t\t\t\t')

							if pointer.pos == start_position:
								break
							if pointer.pos == start_position_2:
								# hex='blue'
								path.append(SVG.line_to(pointer.pos))
								path_points_count += 1
								break
							if start_is_offset: start_position_2 = pointer.pos
							
						else:
							hex = 'red'
							print(f'break {path_index}')
							path.append(SVG.line_to(pointer.pos))
							path_points_count += 1
							path = []
							path_points_count = 0
							break

						i += 1
					
					for p in blocked_pixels:
						xp, yp = p
						pointer.pixels[xp, yp] = False

					if path_points_count >= 2:
						pass
						if path_index == path_index:
							# svg_paths.write(SVG.path_open(path_index, fill='none', stroke=hex))			
							svg_paths.write(SVG.path_open(path_index, fill=hex, stroke=hex))
							svg_paths.write("".join(path))
							is_error_path = hex == 'red' or hex == 'blue'
							if is_error_path: 
								start_points.append(SVG.add_circle(start_position_2, radius=0.5, fill='green', stroke='red', stroke_width=0.05))
								start_points.append(SVG.add_text(Point(start_position_2.x-0.15, start_position_2.y+0.15), path_index, color='darkred'))
							
							svg_paths.write(SVG.path_close(not is_error_path))
							# svg_paths.write("".join(arrows))
							start_points.append(SVG.add_circle(start_position, radius=0.5, fill=hex, stroke='red', stroke_width=0.05))
							start_points.append(SVG.add_text(Point(start_position.x-0.15, start_position.y+0.15), path_index, color='darkred'))
						path_index += 1
		
		svg_paths.write(SVG.group_close())
		paths = svg_paths.getvalue()
		svg_paths.close()
		# paths += ''.join(start_points)
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

	# def trace(image: Image, smooth_range: int):
	# 	svg_data: StringIO = StringIO()
		
	# 	image = image.convert("RGB")
	# 	collumns: int = math.ceil(image.width/UFragment.size) #ширина изображения в фрагментах

	# 	start_time = time.time()
	# 	fragments = UAnalyzer.analyze(image)
	# 	end_time = time.time()
	# 	analyzing_time = end_time - start_time
	# 	print(f"\n{C.BOLD}Analyzing{C.END}:\t\t{analyzing_time:.3f} sec ({analyzing_time/60:.1f} min) ({len(fragments)} frgmts)")

	# 	# for f in fragments:
	# 	# 	for c in list(f.colors):
	# 	# 		r, g, b = c.split(',')
	# 	# 		if int(r) > 200 and int(g) > 200 and int(b) > 200: del f.colors[c]

	# 	pointer: UPointer = UPointer(image)

	# 	# svg_data.write(SVG.svg_open(width, height))
	# 	svg_data.write(SVG.paths_group_open())

	# 	smooth_range_x = smooth_range
	# 	smooth_range_y = smooth_range

	# 	start_fragments = []
	# 	removing_time = 0
	# 	while len(fragments) > 0:
	# 		fragment = fragments[next(iter(fragments))]
	# 		start_fragments.append(fragment)
	# 		for color in list(fragment.colors.keys()):
	# 			path = []
	# 			controll_points = []
	# 			linear_points = []
	# 			arrows = []
	# 			r, g, b = color.split(',')
	# 			pointer.color = (int(r), int(g), int(b))

	# 			#hack
	# 			if not pointer.calculate_start_position(fragment.position, Point(fragment.position.x + UFragment.size-1, fragment.position.y + UFragment.size-1)):
	# 				index = int(fragment.position.y/UFragment.size)*collumns+int(fragment.position.x/UFragment.size)
	# 				if index in fragments: del fragments[index]
	# 				print(f"{index} continue.................")
	# 				continue

	# 			# print(f'{fragment.index} {pointer.arrow.value}')

	# 			start_point = pointer.pos
	# 			prev_corner = start_point

	# 			hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
	# 			# svg_data.write(SVG.path_open(stroke=hex))
	# 			# path.append(SVG.path_open(fragment, hex, stroke=hex))
	# 			path.append(SVG.path_open(hex, stroke=hex))

	# 			path.append(SVG.move_to(start_point))
	# 			# svg_data.write(SVG.path_open(fragment, hex, stroke=hex))              
	# 			# svg_data.write(SVG.move_to(start_point))

	# 			corners_count = 1
	# 			corners = [0,0,0,0]
	# 			corners[0] = start_point
	# 			while True:
	# 				prev_point = pointer.pos

	# 				start_time = time.time()
	# 				index = int(pointer.pos.y/UFragment.size)*collumns+int(pointer.pos.x/UFragment.size)
	# 				if index in fragments:
	# 					f = fragments[index]
	# 					if color in f.colors: del f.colors[color]
	# 					if len(f.colors) == 0: del fragments[index] #FIXME: recalc hash
	# 				end_time = time.time()
	# 				removing_time += (end_time - start_time)

	# 				# pointer.perform_move()
	# 				pointer.perform_move_universal()
					
	# 				# arrows.append(SVG.add_fragment(pointer.pos, 1, 1, stroke='green'))
	# 				# arrows.append(SVG.add_text(pointer.pos, pointer.arrow.value, color='green'))

	# 				if pointer.arrow_is_changed:
	# 					if (abs(prev_point.x - prev_corner.x) >= smooth_range_x or
	# 						abs(prev_point.y - prev_corner.y) >= smooth_range_y):
								
	# 						path.append(SVG.line_to(prev_point))

	# 						#for error test
	# 						if corners_count >= 100:
	# 							path.append(SVG.path_close())
	# 							svg_data.write("".join(path))
	# 							# svg_data.write("".join(arrows))
	# 							break

	# 						# if corners_count % 4 == 1: corners[1] = prev_point
	# 						# if corners_count % 4 == 2: corners[2] = prev_point
	# 						# if corners_count % 4 == 3: corners[3] = prev_point
	# 						# if corners_count % 4 == 0:
	# 						# 	p0, c1, c2, p1 = UTracer.get_control_points(corners[0], corners[1], corners[2], corners[3])
	# 						# 	path.append(SVG.curve_to(p0, c1, c2, p1))
	# 						# 	linear_points.append(corners[0])
	# 						# 	linear_points.append(corners[1])
	# 						# 	linear_points.append(corners[2])
	# 						# 	linear_points.append(corners[3])
	# 						# 	controll_points.append(SVG.add_circle(p0, fill="blue"))
	# 						# 	controll_points.append(SVG.add_circle(c1))
	# 						# 	controll_points.append(SVG.add_circle(c2))
	# 						# 	controll_points.append(SVG.add_circle(p1, fill="blue"))
	# 						# 	corners[0] = p1

	# 						# if corners_count % 3 == 1: corners[1] = prev_point
	# 						# if corners_count % 3 == 2: corners[2] = prev_point
	# 						# if corners_count % 3 == 0:
	# 						# 	temp1 = UTracer.calc_point(corners[0], corners[1], corners[2])
	# 						# 	tension = 2
	# 						# 	c1 = temp1*(1-tension) + corners[1]*tension
	# 						# 	c1 = c1.round(2)
	# 						# 	path.append(SVG.add_quadratic_bezier(corners[0], c1, corners[2]))
	# 						# 	linear_points.append(corners[0])
	# 						# 	linear_points.append(corners[1])
	# 						# 	linear_points.append(corners[2])
	# 						# 	controll_points.append(SVG.add_circle(corners[0], fill="blue"))
	# 						# 	controll_points.append(SVG.add_circle(c1))
	# 						# 	controll_points.append(SVG.add_circle(corners[2], fill="blue"))
	# 						# 	corners[0] = corners[2]

	# 						prev_corner = prev_point

	# 						corners_count += 1                      
	# 						if corners_count % 10 == 0:
	# 							path.append('\n\t\t\t\t')             

	# 				if pointer.pos == start_point:
	# 					break
			
	# 			path.append(SVG.path_close())
	# 			if corners_count >= 2:
	# 				# svg_data.write(SVG.path_open(fragment, "none", "blue"));
	# 				# ii = 0
	# 				# for p in linear_points:
	# 				# 	if ii == 0:
	# 				# 		svg_data.write(SVG.move_to(p));
	# 				# 	else:
	# 				# 		svg_data.write(SVG.line_to(p));
	# 				# 	ii += 1
	# 				# svg_data.write(SVG.path_close());

	# 				svg_data.write("".join(path))
	# 				# svg_data.write("".join(arrows))

	# 				# svg_data.write("".join(controll_points) + "\n")
	# 				# pass
		
	# 	print(f'removing {removing_time:.4f} sec')

	# 	svg_data.write(SVG.group_close())
	# 	# svg_data.write(SVG.svg_close())
		

	# 	print(f"\nPointer position changes: {pointer.moves_count:,}")

	# 	svg_fragments = ''
	# 	# svg_fragments = UTracer.draw_fragments(start_fragments) #draw start fragments

	# 	result = svg_data.getvalue() + svg_fragments
	# 	svg_data.close()
	# 	return result