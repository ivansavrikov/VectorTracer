from core.Point import Point

	

class BuilderSVG:

	def svg_open(width: int, height: int):
		return (
			f'<svg\n'
			f'\twidth="{width}"\n'
			f'\theight="{height}"\n'
			f'\tviewBox="0 0 {width} {height}"\n'
			f'\txmlns="http://www.w3.org/2000/svg"\n'
			f'\txmlns:xlink="http://www.w3.org/1999/xlink">\n'
		)

	def group_open():
		return '\n\t<g>\n'
		
	def group_close():
		return '\t</g>\n'

	def move_to(point: Point):
		return f'M {point.x} {point.y} '

	def line_to(point: Point):
		return f'L {point.x} {point.y} '

	def paths_group_open():
		return (
			f'\n\t<g\n'
			f'\t\tfill-opacity="1"\n'
			f'\t\tstroke-linejoin="mitter"\n'
			f'\t\tstroke-opacity="1"\n'
			f'\t\tstroke-width="1.5">\n\n'
		)

	def path_open(fill='none', stroke='black', opacity='1'):
		return (
			f'\t\t<path\n'
			f'\t\t\tfill="{fill}"\n'
			# f'\t\t\tfill-opacity="{opacity}"\n'
			f'\t\t\tstroke="{stroke}"\n'
			# f'\t\t\tstroke-opacity="{opacity}"\n'
			# f'\t\t\tstroke-width="1.5"\n'
			f'\t\t\td="'
		)
		
	def path_close():
		return 'Z"/>\n\n'

	def add_circle(center: Point, radius=5):
		return (
			f'\t\t<circle\n'
			f'\t\t\tcx="{center.x}"\n'
			f'\t\t\tcy="{center.y}"\n'
			f'\t\t\tr="{radius}"\n'
			f'\t\t\tfill="red"\n'
			f'\t\t\tfill-opacity="0.8"\n'
			f'\t\t\tstroke="none"\n'
			f'\t\t\tstroke-width="0"/>\n'
		)

	def fragments_group_open():
		return (
			f'\n\t<g\n'
			f'\t\tfill-opacity="1"\n'
			f'\t\tstroke-opacity="1"\n'
			f'\t\tfont-size="2"\n'
			f'\t\tfont-family="Calibri">\n\n'
		)

	def add_fragment(pos: Point, width, height, fill='none'):
		return (
			f'\t\t<rect '
			f'x="{pos.x-0.5}" '
			f'y="{pos.y-0.5}" '
			f'width="{width}" '
			f'height="{height}" '
			f'stroke="black" '
			f'stroke-width="0.1" '
			f'fill="{fill}"/>\n'
		)

	def add_quadratic_bezier(control: Point, end: Point):
		return f"Q {control.x} {control.y} {end.x} {end.y} "

	def add_smooth_quadratic_Bezier(end: Point):
		return f"T {end.x} {end.y} "

	def add_text(pos: Point, text: str):
		return (
			f'\t\t<text '
			f'x="{pos.x}" '
			f'y="{pos.y}" '
			f'fill="black"'
			f'>{text}</text>\n'
		)

	def add_image(image_data: str, width, height):
		return (
			f'\n\t<image '
			f'x="{-0.5}" '
			f'y="{-0.5}" '
			f'width="{width}" '
			f'height="{height}" '
			f'image-rendering="pixelated" '
			f'xlink:href="data:image/png;base64,{image_data}"/>\n'
		)

	def svg_close():
		return '\n</svg>'