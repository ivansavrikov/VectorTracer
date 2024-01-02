from PIL import Image


#Возмножный рефакторинг названия класса, как "ImageFilter"

class ImagePreparer:

    def prepare(image: Image) -> Image:
        '''Подготовливает изображение, для трассировки'''

        background_color = (255, 255, 255)
        new_image = Image.new('RGB', image.size, background_color)
        mask = image.convert("RGBA")
        new_image.paste(image, (0, 0), mask)
        
        new_image = new_image.convert('L') #подумать над convert('1')

        return new_image