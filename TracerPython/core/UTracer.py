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

class UTracer:

	def trace(image: Image, smooth_range: int):
		svg_data: StringIO = StringIO()
		
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
		# svg_data.write(SVG.svg_open(width, height))
		svg_data.write(SVG.paths_group_open())

		smooth_range_x = smooth_range
		smooth_range_y = smooth_range

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

				hex = '#{:02x}{:02x}{:02x}'.format(*pointer.color)
				svg_data.write(SVG.path_open(hex, stroke=hex))               
				svg_data.write(SVG.move_to(first))

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
						print(f'Lonely pixel: {pointer.pos.x} {pointer.pos.y}')
						break
					
					if pointer.arrow_is_changed:
						# print(pointer.arrow.value)
						potential = prev
						if (abs(potential.x - corner.x) >= smooth_range_x or 
							abs(potential.y - corner.y) >= smooth_range_y):
							corner = potential
							svg_data.write(SVG.line_to(corner))

							corners_count += 1                      
							if corners_count % 10 == 0:
								svg_data.write('\n\t\t\t\t')                  

					if pointer.pos == first:
						break
			
				svg_data.write(SVG.path_close())
		
		svg_data.write(SVG.group_close())		
		# svg_data.write(SVG.svg_close())

		print(f"\nPointer position changes: {pointer.moves_count:,}")

		result = svg_data.getvalue()
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
	
	def draw_fragments(image: Image):
		svg_data: StringIO = StringIO()
		
		image = image.convert("RGB")
		fragments = UAnalyzer.analyze(image)

		svg_data.write(SVG.fragments_group_open())
		for f in fragments:
			svg_data.write(SVG.add_fragment(f.position, UFragment.size, UFragment.size, fill='none'))
			svg_data.write(SVG.add_text(Point(f.position.x, f.position.y+UFragment.size/2), f'{f.index}'))
		svg_data.write(SVG.group_close())

		result = svg_data.getvalue()
		svg_data.close()
		return result