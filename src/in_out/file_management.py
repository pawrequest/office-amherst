import os
import subprocess
from pathlib import Path
from typing import Any, Protocol, Tuple

from comtypes.client import CreateObject
from docx2pdf import convert as convert_word


# convert doc to pdf
class PdfConverter(Protocol):
    def convert(self, out_file: Path):
        ...


class WordConverter:
    def convert(self, doc_file: Path):
        try:
            convert_word(doc_file, output_path=doc_file.parent, keep_active=True)
            print(f"Converted {doc_file}")
        except Exception as e:
            raise e


class LibreConverter:
    def convert(self, doc_file: Path):
        try:
            subprocess.run(f'soffice --headless --convert-to pdf {str(doc_file)} --outdir {str(doc_file.parent)}')
            print(f"Converted {doc_file}")
            return True
        except Exception as e:
            ...


# open doc

class DocumentOpenerProtocol(Protocol):
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        ...


class WordOpener:
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc = word.Documents.Open(str(doc_path))
            return word, word_doc
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None


class LibreOpener:
    def open_document(self, doc_path: Path) -> Tuple[Any, Any]:
        try:
            process = subprocess.Popen(['soffice', str(doc_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process, None  # Returning None as the second element as LibreOffice doesn't provide a document object
        except Exception as e:
            raise e


def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
        return True
    except Exception as e:
        print(f"Failed to print: {e}")
        return False
