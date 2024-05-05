import base64
from io import BytesIO, StringIO
from PIL import Image
from core.BuilderSVG import BuilderSVG as SVG
from core.Point import Point
from core.UPointer import UPointer
import math
from core.UAnalyzer import UAnalyzer
from core.UFragment import UFragment
from core.Exceptions import MyCustomException
from core.Console import Console as C
import time

class UTracer:

	def trace(image: Image, smooth_range: int):
		svg_data: StringIO = StringIO()
		
		image = image.convert("RGB")
		collumns: int = math.ceil(image.width/UFragment.size) #ширина изображения в фрагментах

		start_time = time.time()
		fragments = UAnalyzer.analyze(image)
		end_time = time.time()
		analyzing_time = end_time - start_time
		print(f"\n{C.BOLD}Analyzing{C.END}:\t\t{analyzing_time:.3f} sec ({analyzing_time/60:.1f} min) ({len(fragments)} frgmts)")

		# for f in fragments:
		# 	for c in list(f.colors):
		# 		r, g, b = c.split(',')
		# 		if int(r) > 200 and int(g) > 200 and int(b) > 200: del f.colors[c]

		pointer: UPointer = UPointer(image)

		# svg_data.write(SVG.svg_open(width, height))
		svg_data.write(SVG.paths_group_open())

		smooth_range_x = smooth_range
		smooth_range_y = smooth_range

		start_fragments = []
		removing_time = 0
		while len(fragments) > 0:
			fragment = fragments[next(iter(fragments))]
			start_fragments.append(fragment)
			for color in list(fragment.colors.keys()):
				r, g, b = color.split(',')
				pointer.color = (int(r), int(g), int(b))
				pointer.calculate_start_position(fragment.position, Point(fragment.position.x + UFragment.size-1, fragment.position.y + UFragment.size-1))

				start_point = pointer.pos
				prev_corner = start_point

				hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
				# svg_data.write(SVG.path_open(stroke=hex))
				svg_data.write(SVG.path_open(hex, stroke=hex))              
				svg_data.write(SVG.move_to(start_point))

				corners_count = 1
				while True:
					prev_point = pointer.pos

					start_time = time.time()
					index = int(pointer.pos.y/UFragment.size)*collumns+int(pointer.pos.x/UFragment.size)
					if index in fragments:
						f = fragments[index]
						if color in f.colors: del f.colors[color]
						if len(f.colors) == 0: del fragments[index] #FIXME: recalc hash
					end_time = time.time()
					removing_time += (end_time - start_time)

					pointer.perform_move()
					
					if pointer.arrow_is_changed:
						if (abs(prev_point.x - prev_corner.x) >= smooth_range_x or 
							abs(prev_point.y - prev_corner.y) >= smooth_range_y):
							svg_data.write(SVG.line_to(prev_point))
							prev_corner = prev_point

							corners_count += 1                      
							if corners_count % 10 == 0:
								svg_data.write('\n\t\t\t\t')                  

					if pointer.pos == start_point:
						break
			
				svg_data.write(SVG.path_close())
		
		print(f'removing {removing_time:.4f} sec')

		svg_data.write(SVG.group_close())		
		# svg_data.write(SVG.svg_close())

		print(f"\nPointer position changes: {pointer.moves_count:,}")

		svg_fragments = ''
		# svg_fragments = UTracer.draw_fragments(start_fragments) #draw start fragments

		result = svg_data.getvalue() + svg_fragments
		svg_data.close()
		return result
	
	def put_image(image: Image):
		svg_image: StringIO = StringIO()
		
		image_bytes_io = BytesIO()
		image.save(image_bytes_io, format="PNG")
		image_bytes = image_bytes_io.getvalue()
		image_data = base64.b64encode(image_bytes).decode('utf-8')

		svg_image.write(SVG.add_image(image_data, image.width, image.height))

		result = svg_image.getvalue()
		svg_image.close()
		return result
	
	def draw_fragments(fragments: list):
		svg_data: StringIO = StringIO()
		
		# image = image.convert("RGB")
		# fragments = UAnalyzer.analyze(image)

		svg_data.write(SVG.fragments_group_open())
		for f in fragments:
			svg_data.write(SVG.add_fragment(f.position, UFragment.size, UFragment.size, fill='none'))
			svg_data.write(SVG.add_text(Point(f.position.x, f.position.y+UFragment.size/2), f'{f.index}'))
		svg_data.write(SVG.group_close())

		result = svg_data.getvalue()
		svg_data.close()
		return result