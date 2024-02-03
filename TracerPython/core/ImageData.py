from PIL import Image
from typing import List
from core.Fragment import Fragment


class ImageData:
    def __init__(self, image: Image):
        self.image = image
        self.fragments: List[Fragment] = [] #подумать над двумерной матрицей, в соответствии с изображением