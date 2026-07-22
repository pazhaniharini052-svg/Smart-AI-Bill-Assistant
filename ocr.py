import easyocr
import numpy as np
from PIL import Image


reader = easyocr.Reader(
    ['en'],
    gpu=False
)


def extract_text(image):

    if isinstance(image, Image.Image):
        image = np.array(image)

    result = reader.readtext(
        image,
        detail=0
    )

    return "\n".join(result)