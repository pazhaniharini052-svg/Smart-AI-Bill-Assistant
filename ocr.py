from PIL import Image
import easyocr
import numpy as np

# Load EasyOCR model once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image):
    if isinstance(image, Image.Image):
        image = np.array(image)

    result = reader.readtext(image)

    text = "\n".join([item[1] for item in result])

    return text