from PIL import Image



class ImageData:
    def __init__(self, image: Image):
        self.image = image
        self.fragments: list = [] #подумать над двумерной матрицей, в соответствии с изображением