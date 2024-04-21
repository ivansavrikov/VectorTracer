from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans

def quantize_colors(image: Image, num_colors):
    # Получение размеров изображения
    width, height = image.size
    
    # Преобразование изображения в массив пикселей в формате RGB
    pixels = np.array(image)
    
    # Преобразование цветового пространства из RGB в BGR для OpenCV
    pixels_bgr = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)

    # Преобразование массива пикселей в одномерный массив
    pixels_flatten = pixels_bgr.reshape(-1, 3)

    # Создание модели KMeans с указанным количеством цветов
    kmeans = KMeans(n_clusters=num_colors, random_state=42)

    # Применение алгоритма кластеризации
    kmeans.fit(pixels_flatten)

    # Получение центроидов кластеров
    colors = kmeans.cluster_centers_.astype(int)

    # Присваивание каждому пикселю ближайшего цвета из центроидов
    labels = kmeans.labels_
    quantized_pixels_flatten = colors[labels]

    # Преобразование массива пикселей обратно в формат изображения
    quantized_image = quantized_pixels_flatten.reshape((height, width, 3))

    # Преобразование цветового пространства обратно в RGB для PIL
    quantized_image_rgb = cv2.cvtColor(quantized_image.astype('uint8'), cv2.COLOR_BGR2RGB)
    
    # Создание объекта изображения PIL
    quantized_pil_image = Image.fromarray(quantized_image_rgb)

    return quantized_pil_image