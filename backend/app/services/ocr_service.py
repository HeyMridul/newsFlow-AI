import io
from PIL import Image, ImageOps
import pytesseract


def extract_text_from_image(image_bytes: bytes, lang: str = "eng+hin") -> str:
    image = Image.open(io.BytesIO(image_bytes))

    # Basic preprocessing: convert to grayscale, auto-orient based on EXIF
    image = ImageOps.exif_transpose(image)
    image = image.convert("L")

    text = pytesseract.image_to_string(image, lang=lang)

    if not text.strip():
        raise ValueError("Could not extract any text from this image.")

    return text.strip()