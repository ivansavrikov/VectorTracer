from PIL import Image
import math

def find_closest_color(pixel, colors):
    min_distance = float('inf')
    closest_color = None
    
    for color in colors:
        distance = math.sqrt(
            (color[0] - pixel[0]) ** 2 +
            (color[1] - pixel[1]) ** 2 +
            (color[2] - pixel[2]) ** 2
        )
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

def recolor_image(image, target_colors):
    image = image.convert('RGB')
    pixels = image.load()
    
    width, height = image.size
    for i in range(width):
        for j in range(height):
            pixel = pixels[i, j]
            closest_color = find_closest_color(pixel, target_colors)
            pixels[i, j] = tuple(closest_color)
    return image