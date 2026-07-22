from paddleocr import PaddleOCR
from PIL import Image
import numpy as np


ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)


def extract_text(image):

    if isinstance(image, Image.Image):
        image = np.array(image)


    result = ocr.ocr(
        image,
        cls=True
    )


    text = ""

    for line in result:

        for item in line:

            text += item[1][0] + "\n"


    return text