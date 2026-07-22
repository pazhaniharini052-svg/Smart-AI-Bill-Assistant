import pytesseract
import numpy as np
from PIL import Image


def extract_text(image):

    if isinstance(image, Image.Image):
        image = np.array(image)

    text = pytesseract.image_to_string(
        image
    )

    return text