# banned_detector/utils/ocr/image_ocr.py

from typing import Dict, Any
from PIL import Image

try:
    import pytesseract

    # Windows path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

except Exception:
    pytesseract = None


def extract_text_from_image(image_path: str) -> Dict[str, Any]:
    if pytesseract is None:
        return {
            "text": "",
            "success": False,
            "error": "pytesseract is not installed.",
        }

    try:
        image = Image.open(image_path).convert("RGB")
        text = pytesseract.image_to_string(image)

        return {
            "text": text.strip(),
            "success": True,
            "error": None,
        }

    except Exception as exc:
        return {
            "text": "",
            "success": False,
            "error": str(exc),
        }