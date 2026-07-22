from PIL import Image
import pytesseract

# Update this path if your installation is elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)

    return pytesseract.image_to_string(image)