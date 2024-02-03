from core.Point import Point



class BuilderSVG:

    def svg_open(self, width: int, height: int):
        self.svg_code = f'''<svg
    width="{width-1}" height="{height-1}" 
    viewBox="0 0 {width-1} {height-1}" 
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">'''

    def open_group(self):
        self.svg_code += '''\n\t<g fill-rule="evenodd" fill="black" stroke="none" stroke-width="0" >\n'''
        
    def close_group(self):
        self.svg_code += '\n\t</g>'

    def add_move(self, point: Point):
        self.path_data += f'M {point.x} {point.y} '

    def add_line(self, point: Point):
        self.path_data += f'L {point.x} {point.y} '

    def add_path(self, fill='black', stroke='black', opacity='1', close='Z'):
        self.svg_code += f'\n\t\t<path fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="1" stroke-linejoin="miter" \n\t\td="{self.path_data}{close}"/> \n'
        self.path_data = ''

    def add_circle(self, center: Point, radius=5):
        self.svg_code += f'''\n\t<circle cx="{center.x}" cy="{center.y}" r="{radius}" stroke="none" stroke-width="0" fill="red" fill-opacity="0.8"/>'''

    def add_rectangle(self, pos: Point, width, height, fill='none'):
        self.svg_code += f'''\n\t<rect x="{pos.x}" y="{pos.y}" width="{width}" height="{height}" fill="{fill}" fill-opacity="0.2" stroke="red" stroke-opacity="0.8" stroke-width="0.5" />'''

    def add_quadratic_bezier(self, control: Point, end: Point):
        self.path_data += f"Q {control.x} {control.y} {end.x} {end.y} "

    def add_smooth_quadratic_Bezier(self, end: Point):
        self.path_data += f"T {end.x} {end.y} "

    def add_text(self, pos: Point, text: str):
        self.svg_code += f'''\n\t<text x="{pos.x}" y="{pos.y}" font-family="Arial" font-size="6" fill="red">{text}</text>'''

    def add_image(self, path: str, width, height):
        self.svg_code += f'''<image xlink:href="{path}" x="0" y="0" width="{width}" height="{height}" />'''

    def svg_close(self):
        self.svg_code += '\n</svg>'

    def __init__(self):
        self.path_data: str = ''
        self.svg_code: str = ''