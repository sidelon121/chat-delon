import os
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader

UPLOAD_FOLDER = "uploads"

class FileProcessor:
    def __init__(self):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

    def save_file(self, file):
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename, filepath

    def analyze_file(self, filepath, mime_type):
        if "image" in mime_type:
            return self.analyze_image(filepath)
        elif "pdf" in mime_type:
            return self.analyze_pdf(filepath)
        else:
            return "File type tidak dikenali."

    def analyze_image(self, filepath):
        try:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            if text.strip() == "":
                return "Tidak ada teks yang terdeteksi."
            return text
        except Exception as e:
            return f"[Image OCR Error] {str(e)}"

    def analyze_pdf(self, filepath):
        try:
            reader = PdfReader(filepath)
            extracted = ""
            for page in reader.pages:
                extracted += page.extract_text() or ""
            if extracted.strip() == "":
                return "PDF tidak berisi teks yang dapat diekstrak."
            return extracted
        except Exception as e:
            return f"[PDF Error] {str(e)}"
