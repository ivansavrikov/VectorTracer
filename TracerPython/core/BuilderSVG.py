from PIL import Image
from core.Pointer import Pointer

def raster_to_svg(image: Image) -> str:
    width, height = image.size
    path_lines_points: str = ''

    pointer = Pointer(image)
    start_x, start_y = pointer.x, pointer.y

    while True:
        prev_x, prev_y = pointer.x, pointer.y
        pointer.perform_move()
        if pointer.x == start_x and pointer.y == start_y:
            break
        if pointer.arrow_is_changed:
            path_lines_points += f"L {prev_x} {prev_y} "

    scale = 3
    svg_code = f"""<svg width="{width*scale}" height="{height*scale}" viewBox="0 0 {width*scale} {height*scale}" xmlns="http://www.w3.org/2000/svg">
    <g transform="scale({scale})">
        <path d="M {start_x} {start_y} {path_lines_points}Z" fill="red" stroke="black" stroke-width="0"/>
    </g>
</svg>"""
    return svg_code