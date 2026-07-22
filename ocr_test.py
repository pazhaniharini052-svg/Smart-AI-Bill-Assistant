from paddleocr import PaddleOCR

ocr = PaddleOCR(lang="en")

result = ocr.ocr(
    r"C:\Users\pazha\OneDrive\画像\Screenshots\Screenshot 2026-07-19 114426.png"
)

for line in result:
    print(line)