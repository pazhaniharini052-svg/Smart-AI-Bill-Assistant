from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def extract_text(image):
    if isinstance(image, Image.Image):
        image = np.array(image)

    result = ocr.ocr(image, cls=True)

    text = ""

    if result and result[0]:
        for line in result[0]:
            text += line[1][0] + "\n"

    return text