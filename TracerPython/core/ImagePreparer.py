from PIL import Image
import math
from core.Point import Point

#ВОЗМОЖЕН РЕФАКТОРИНГ
class ImagePreparer:

    def process_image(img):
        # Проверить, если изображение имеет альфа-канал (прозрачность)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Создать новое изображение с белым фоном
            new_img = Image.new("RGB", img.size, (255, 255, 255))
            new_img.paste(img, mask=img.split()[3])  # Вставить с альфа-каналом в качестве маски
        else:
            new_img = img.convert("RGB")  # Преобразовать в режим RGB, если изображение не имеет альфа-канала
        
        return new_img