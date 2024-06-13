from core.Point import Point
from datetime import date

class BuilderSVG:

	def svg_open(width: int, height: int):
		return (
			f'<svg\n'
			f'\twidth="{width}"\n'
			f'\theight="{height}"\n'
			f'\tviewBox="-1 -1 {width+1} {height+1}"\n'
			# f'\tviewBox="0 0 {width+1} {height+1}"\n'
			f'\txmlns="http://www.w3.org/2000/svg"\n'
			f'\txmlns:xlink="http://www.w3.org/1999/xlink">\n'
		)

	def metadata():
		return (
			f'\n\t<metadata>\n'
			f'\tCreated by SpiderTracer 1.0, developed by Ivan Savrikov 2023-{date.today().year}\n'
			f'\t</metadata>\n'
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
			f'\t\tstroke-width="1">\n\n'
		)

	def path_open(index='-1', fill='none', stroke='black', opacity='1'):
		return (
			f'\t\t<path '
			f'id="{index}"\n'
			f'\t\t\tfill="{fill}"\n'
			# f'\t\t\tfill-opacity="{opacity}"\n'
			f'\t\t\tstroke="{stroke}"\n'
			# f'\t\t\tstroke-opacity="{opacity}"\n'
			# f'\t\t\tstroke-width="1.5"\n'
			f'\t\t\td="'
		)
		
	def path_close(is_closed=True):
		if is_closed: return 'Z"/>\n\n'
		else: return '"/>\n\n'

	def add_circle(center: Point, radius=0.3, fill="red", stroke='none', stroke_width=0):
		return (
			f'\t\t<circle '
			f'cx="{center.x}" '
			f'cy="{center.y}" '
			f'r="{radius}" '
			f'fill="{fill}" '
			f'fill-opacity="0.7" '
			f'stroke="{stroke}" '
			f'stroke-width="{stroke_width}"/>\n'
		)

	def fragments_group_open():
		return (
			f'\n\t<g\n'
			f'\t\tfill-opacity="1"\n'
			f'\t\tstroke-opacity="1"\n'
			f'\t\tfont-size="0.5"\n'
			f'\t\tfont-family="Calibri">\n\n'
		)

	def add_fragment(pos: Point, width, height, fill='none', stroke='purple'):
		return (
			f'\t\t<rect '
			f'x="{pos.x-0.5}" '
			f'y="{pos.y-0.5}" '
			f'width="{width}" '
			f'height="{height}" '
			f'stroke="{stroke}" '
			f'stroke-width="0.01" '
			f'fill="{fill}"/>\n'
		)

	def curve_to(p0, c1, c2, p1):
		# return f"C {c1.x:.0f} {c1.y:.0f} {c2.x:.0f} {c2.y:.0f} {p1.x} {p1.y} "
		return f"C {BuilderSVG.format_number(c1.x)} {BuilderSVG.format_number(c1.y)} {BuilderSVG.format_number(c2.x)} {BuilderSVG.format_number(c2.y)} {p1.x} {p1.y} "

	def add_quadratic_bezier(start: Point, control: Point, end: Point):
		return f"Q {control.x} {control.y} {end.x} {end.y} "

	def add_smooth_quadratic_Bezier(end: Point):
		return f"T {end.x} {end.y} "

	def add_text(pos: Point, text: str, color='purple'):
		return (
			f'\t\t<text '
			f'x="{pos.x}" '
			f'y="{pos.y}" '
			f'fill="{color}" '
			f'font-size="0.5" '
			f'font-family="Calibri"'
			f'>{text}</text>\n'
		)

	def add_image(image_data: str, width, height, pos=Point(0,0)):
		return (
			f'\n\t<image '
			f'opacity="0.5" '
			f'x="{pos.x-0.5}" '
			f'y="{pos.y-0.5}" '
			f'width="{width}" '
			f'height="{height}" '
			f'image-rendering="pixelated" '
			f'xlink:href="data:image/png;base64,{image_data}"/>\n'
		)

	def svg_close():
		return '\n</svg>'
	
	def get_hex_code(r, g, b) -> str:
		return f'#{r:02x}{g:02x}{b:02x}'
	
	def format_number(value):
		return f"{int(value)}" if value.is_integer() else f"{value}"