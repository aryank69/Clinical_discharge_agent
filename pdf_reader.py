import fitz  # PyMuPDF
from pathlib import Path


class PDFReader:
    """
    Reads PDF documents and extracts text.
    """

    def __init__(self):
        pass

    def read_pdf(self, pdf_path: str) -> dict:
        """
        Extract text from PDF.

        Returns:
        {
            "status": "success" | "error",
            "text": extracted_text,
            "pages": page_count,
            "error": error_message
        }
        """

        try:
            pdf_file = Path("C:\Users\Aryan Kalra\Desktop\projects\Clinical_discharge_agent\patient 2 (1).pdf")

            if not pdf_file.exists():
                return {
                    "status": "error",
                    "text": "",
                    "pages": 0,
                    "error": f"File not found: {pdf_path}"
                }

            document = fitz.open(pdf_path)

            all_text = []

            for page_num in range(len(document)):
                page = document.load_page(page_num)

                page_text = page.get_text("text")

                all_text.append(
                    f"\n--- PAGE {page_num + 1} ---\n"
                )
                all_text.append(page_text)

            document.close()

            return {
                "status": "success",
                "text": "\n".join(all_text),
                "pages": len(document),
                "error": None
            }

        except Exception as e:
            return {
                "status": "error",
                "text": "",
                "pages": 0,
                "error": str(e)
            }