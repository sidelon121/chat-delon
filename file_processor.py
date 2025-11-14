import os
import uuid
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import mimetypes

class FileProcessor:
    def __init__(self, upload_folder="uploads"):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def allowed_file(self, filename):
        allowed_extensions = {
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp',
            'pdf', 'txt', 'docx', 'pptx', 'xlsx'
        }
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(self.upload_folder, unique_filename)
            file.save(file_path)
            return unique_filename, file_path
        return None, None
    
    def extract_text_from_pdf(self, file_path):
        """Extract text dari PDF"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, file_path):
        """Extract text dari DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_text_from_image(self, image_path):
        """Extract text dari gambar menggunakan OCR"""
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            return text.strip() if text.strip() else "Tidak ada teks yang terdeteksi dalam gambar."
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def extract_text_from_txt(self, file_path):
        """Extract text dari file teks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                return f"Error reading text file: {str(e)}"
    
    def analyze_file(self, file_path, file_type):
        """Analisis file dan ekstrak kontennya"""
        file_info = {
            'file_type': file_type,
            'file_size': os.path.getsize(file_path),
            'extracted_content': '',
            'analysis_ready': False
        }
        
        try:
            if file_type.startswith('image'):
                file_info['extracted_content'] = self.extract_text_from_image(file_path)
                file_info['analysis_ready'] = True
                
            elif file_type == 'application/pdf':
                content = self.extract_text_from_pdf(file_path)
                file_info['extracted_content'] = content
                file_info['analysis_ready'] = len(content) > 0
                
            elif file_type in ['text/plain']:
                content = self.extract_text_from_txt(file_path)
                file_info['extracted_content'] = content
                file_info['analysis_ready'] = len(content) > 0
                
            elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                content = self.extract_text_from_docx(file_path)
                file_info['extracted_content'] = content
                file_info['analysis_ready'] = len(content) > 0
                
            else:
                file_info['extracted_content'] = f"File type {file_type} tidak didukung untuk analisis mendalam."
                
        except Exception as e:
            file_info['extracted_content'] = f"Error processing file: {str(e)}"
        
        return file_info