import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

from comtypes.client import CreateObject
from docx import Document
from docx2pdf import convert as convert_word


class DocHandler(ABC):
    @abstractmethod
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        raise NotImplementedError

    @abstractmethod
    def to_pdf(self, doc_file: Path) -> Path:
        raise NotImplementedError


class WordHandler(DocHandler):
    # todo use library
    def open_document(self, doc_path: Path) -> Tuple:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc: word.Document = word.Documents.Open(str(doc_path))
            return word, word_doc
        except OSError as e:
            print(f"Is Word installed? Failed to open {doc_path} with error: {e}")
            raise e
        except Exception as e:
            raise e

    def to_pdf(self, doc_file: Path) -> Path:
        try:
            pdf_file = convert_word(doc_file, output_path=doc_file.parent)
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except Exception as e:
            raise e


class LibreHandler(DocHandler):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            process = subprocess.Popen(['soffice', str(doc_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            raise e
        return process, None

    def to_pdf(self, doc_file: Path) -> Path:
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(doc_file)} --outdir {str(doc_file.parent)}')
            outfile = doc_file.with_suffix('.pdf')
            print(f"Converted {outfile}")
            return outfile
        except FileNotFoundError as e:
            print('Is LibreOffice installed?')
        except Exception as e:
            ...


class DocxHandler(DocHandler):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            doc = Document(doc_path)
            return None, doc  # Returning None as there's no application object like in WordHandler
        except Exception as e:
            print(f"Failed to open {doc_path} with error: {e}")
            raise e
