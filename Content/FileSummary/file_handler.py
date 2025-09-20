import os
from django.core.files.storage import default_storage
from docx import Document
import fitz  

class FileContentHandler:
     # Utility class to extract text content from uploaded files (.txt, .docx, .pdf)
    @staticmethod
    def extract_text(uploaded_file):
        saved_path = default_storage.save(f"temp/{uploaded_file.name}", uploaded_file)
        full_path = os.path.join("media", saved_path)

        try:
            if full_path.endswith(".docx"):
                return FileContentHandler._read_docx(full_path)
            elif full_path.endswith(".txt"):
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()
            elif full_path.endswith(".pdf"):
                return FileContentHandler._read_pdf(full_path)
            else:
                raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf files only.")
        
        except UnicodeDecodeError:
            raise ValueError("File encoding is not UTF-8.")
        
        except Exception as e:
            raise ValueError(f"Could not read file: {e}")
        
        finally:
            if os.path.exists(full_path):
                os.remove(full_path)

    @staticmethod
    def _read_docx(path):
        #  extract from .docx file
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def _read_pdf(path):
        # extract from .pdf file
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
