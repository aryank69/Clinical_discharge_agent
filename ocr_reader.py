import pytesseract
from pdf2image import convert_from_path
from pathlib import Path


class OCRReader:
    """
    OCR fallback for scanned PDFs.
    """

    def __init__(self, tesseract_path=None):

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def read_pdf_with_ocr(self, pdf_path: str) -> dict:
        """
        Extract text using OCR.

        Returns:
        {
            "status": "...",
            "text": "...",
            "pages": n,
            "error": ...
        }
        """

        try:

            pdf_file = Path("patient 2 (1).pdf")

            if not pdf_file.exists():
                return {
                    "status": "error",
                    "text": "",
                    "pages": 0,
                    "error": f"{pdf_path} not found"
                }

            images = convert_from_path(pdf_path)

            extracted_text = []

            for page_no, image in enumerate(images):

                page_text = pytesseract.image_to_string(image)

                extracted_text.append(
                    f"\n--- OCR PAGE {page_no + 1} ---\n"
                )

                extracted_text.append(page_text)

            return {
                "status": "success",
                "text": "\n".join(extracted_text),
                "pages": len(images),
                "error": None
            }

        except Exception as e:

            return {
                "status": "error",
                "text": "",
                "pages": 0,
                "error": str(e)
            }