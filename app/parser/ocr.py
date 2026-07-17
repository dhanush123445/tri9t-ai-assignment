import fitz
import pytesseract

from PIL import Image
import io


class OCRParser:

    @staticmethod
    def extract(page):

        pix = page.get_pixmap(dpi=300)

        image = Image.open(io.BytesIO(pix.tobytes("png")))

        return pytesseract.image_to_string(image)